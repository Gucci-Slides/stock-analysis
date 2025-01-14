# services/data_collector/src/collectors/stock_collector.py
import yfinance as yf
import boto3
from datetime import datetime
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests.exceptions import ReadTimeout
import json
import logging
import time
from typing import List
from ..utils.exceptions import retry_with_backoff, APIRateLimitError, ConnectionError
from ..utils.validators import validate_stock_data
from ..utils.logging import setup_logging

class StockDataCollector:
    def __init__(self, s3_bucket, opensearch_endpoint, opensearch_auth):
        self.s3_bucket = s3_bucket
        self.s3_client = boto3.client('s3')
        
        # OpenSearch client with increased timeout
        self.os_client = OpenSearch(
            hosts=[{'host': opensearch_endpoint, 'port': 443}],
            http_auth=opensearch_auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            timeout=30,
            retry_on_timeout=True,
            max_retries=3
        )
        
        self.logger = setup_logging('stock-data-collector')

    def chunks(self, data, chunk_size=100):
        """Split data into chunks"""
        for i in range(0, len(data), chunk_size):
            yield data.iloc[i:i + chunk_size]

    async def check_s3_exists(self, symbol: str, period: str):
        """Check if data exists in S3"""
        try:
            date_str = datetime.now().strftime("%Y/%m/%d")
            key = f'stocks/{symbol}/{date_str}/data_{period}.json'
            
            try:
                self.s3_client.head_object(Bucket=self.s3_bucket, Key=key)
                return True
            except self.s3_client.exceptions.ClientError:
                return False
                
        except Exception as e:
            self.logger.error(f"Error checking S3: {str(e)}")
            return False

    async def check_opensearch_exists(self, symbol: str):
        """Check if data exists in OpenSearch"""
        try:
            index_name = f"stock-data-{datetime.now().strftime('%Y-%m')}"
            
            if not self.os_client.indices.exists(index=index_name):
                return False
                
            # Check for any documents for this symbol
            query = {
                "query": {
                    "term": {
                        "symbol.keyword": symbol
                    }
                },
                "size": 1
            }
            
            result = self.os_client.search(
                index=index_name,
                body=query
            )
            
            return result['hits']['total']['value'] > 0
            
        except Exception as e:
            self.logger.error(f"Error checking OpenSearch: {str(e)}")
            return False

    @retry_with_backoff(retries=3, exceptions=(APIRateLimitError, ConnectionError))
    async def fetch_stock_data(self, symbol: str, period: str = "max", interval: str = "1d"):
        """
        Fetch stock data from Yahoo Finance with retry logic and validation
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            
            # Validate data
            validate_stock_data(df)
            
            self.logger.info(f"Successfully fetched data for {symbol}")
            return df
            
        except Exception as e:
            if "rate limit" in str(e).lower():
                raise APIRateLimitError(f"Rate limit hit for {symbol}: {str(e)}")
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            raise

    async def store_in_s3(self, symbol: str, data, period: str):
        """Store data in S3 with date-based partitioning"""
        try:
            date_str = datetime.now().strftime("%Y/%m/%d")
            key = f'stocks/{symbol}/{date_str}/data_{period}.json'
            
            self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=key,
                Body=data.to_json()
            )
            return key
        except Exception as e:
            self.logger.error(f"Error storing in S3: {str(e)}")
            raise

    async def index_in_opensearch(self, symbol: str, data):
        """Index data in OpenSearch with batching and retry logic"""
        try:
            index_name = f"stock-data-{datetime.now().strftime('%Y-%m')}"
            total_records = len(data)
            records_processed = 0
            
            print(f"\nStarting indexing for {symbol} - Total records: {total_records}")
            
            # Create index if it doesn't exist
            if not self.os_client.indices.exists(index=index_name):
                print("Creating new index:", index_name)
                self.os_client.indices.create(
                    index=index_name,
                    body={
                        "mappings": {
                            "properties": {
                                "symbol": {"type": "keyword"},
                                "timestamp": {"type": "date"},
                                "open": {"type": "float"},
                                "high": {"type": "float"},
                                "low": {"type": "float"},
                                "close": {"type": "float"},
                                "volume": {"type": "long"}
                            }
                        }
                    }
                )

            # Process data in chunks
            chunks = list(self.chunks(data))
            total_chunks = len(chunks)
            
            for chunk_num, chunk in enumerate(chunks, 1):
                retry_count = 0
                max_retries = 3
                chunk_size = len(chunk)
                
                while retry_count < max_retries:
                    try:
                        # Prepare bulk indexing payload
                        bulk_data = []
                        for timestamp, row in chunk.iterrows():
                            bulk_data.append({
                                "index": {
                                    "_index": index_name,
                                    "_id": f"{symbol}-{timestamp.isoformat()}"
                                }
                            })
                            bulk_data.append({
                                "symbol": symbol,
                                "timestamp": timestamp.isoformat(),
                                "open": float(row['Open']),
                                "high": float(row['High']),
                                "low": float(row['Low']),
                                "close": float(row['Close']),
                                "volume": int(row['Volume'])
                            })

                        # Bulk index the chunk
                        if bulk_data:
                            self.os_client.bulk(body=bulk_data)
                        
                        records_processed += chunk_size
                        percentage_complete = (records_processed / total_records) * 100
                        
                        print(f"Progress: {percentage_complete:.2f}% complete "
                              f"(Chunk {chunk_num}/{total_chunks}, "
                              f"Records: {records_processed}/{total_records})")
                        break  # Success, exit retry loop
                        
                    except ReadTimeout:
                        retry_count += 1
                        if retry_count == max_retries:
                            raise
                        print(f"Timeout on chunk {chunk_num}/{total_chunks}, "
                              f"retrying... ({retry_count}/{max_retries})")
                        time.sleep(2 ** retry_count)  # Exponential backoff
                
                # Small delay between chunks
                time.sleep(1)
                
            print(f"\nIndexing completed for {symbol}!")
            print(f"Total records indexed: {records_processed}")
            
        except Exception as e:
            self.logger.error(f"Error indexing in OpenSearch: {str(e)}")
            raise

    async def collect_and_store(self, symbol: str, period: str = "max", interval: str = "1d"):
        """Main method to collect and store data"""
        try:
            print(f"\nProcessing {symbol}...")
            
            # Check if data exists
            s3_exists = await self.check_s3_exists(symbol, period)
            os_exists = await self.check_opensearch_exists(symbol)
            
            if s3_exists and os_exists:
                print(f"Data for {symbol} already exists in both S3 and OpenSearch. Skipping...")
                return {
                    "symbol": symbol,
                    "status": "skipped",
                    "reason": "data_exists"
                }
            
            # Fetch data
            print(f"Fetching data for {symbol}...")
            data = await self.fetch_stock_data(symbol, period, interval)
            
            # Store in S3 if needed
            s3_key = None
            if not s3_exists:
                print(f"Storing {symbol} data in S3...")
                s3_key = await self.store_in_s3(symbol, data, period)
            else:
                print(f"S3 data exists for {symbol}, skipping S3 storage...")
            
            # Index in OpenSearch if needed
            if not os_exists:
                print(f"Indexing {symbol} data in OpenSearch...")
                await self.index_in_opensearch(symbol, data)
            else:
                print(f"OpenSearch data exists for {symbol}, skipping indexing...")
            
            return {
                "symbol": symbol,
                "period": period,
                "interval": interval,
                "s3_location": f"s3://{self.s3_bucket}/{s3_key}" if s3_key else "existing",
                "timestamp": datetime.now().isoformat(),
                "records": len(data),
                "status": "completed",
                "s3_updated": not s3_exists,
                "opensearch_updated": not os_exists
            }
            
        except Exception as e:
            self.logger.error(f"Error in collect_and_store: {str(e)}")
            raise