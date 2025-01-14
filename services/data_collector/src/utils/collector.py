# services/data_collector/src/utils/collector.py
from ..storage.s3 import S3Storage
from ..storage.elasticsearch_client import ElasticsearchClient
import yfinance as yf
from datetime import datetime

class StockDataCollector:
    def __init__(self):
        self.s3_storage = S3Storage('your-bucket-name')
        self.es_client = ElasticsearchClient(['your-es-host'])

    async def get_stock_data(self, symbol: str, period: str = "1d"):
        try:
            # Fetch data from Yahoo Finance
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            
            # Store in S3
            await self.s3_storage.store_stock_data(symbol, df)
            
            # Store in Elasticsearch
            data_dict = df.reset_index().to_dict('records')
            await self.es_client.store_stock_data(symbol, data_dict)
            
            return {
                "symbol": symbol,
                "data": data_dict,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Error collecting/storing data for {symbol}: {str(e)}")