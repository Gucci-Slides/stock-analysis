# services/data_collector/src/run_collector.py
import asyncio
from collectors.stock_collector import StockDataCollector
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()

async def main():
    # Initialize collector
    collector = StockDataCollector(
        s3_bucket=os.getenv('S3_BUCKET'),
        opensearch_endpoint=os.getenv('OPENSEARCH_ENDPOINT'),
        opensearch_auth=(os.getenv('OPENSEARCH_USER'), os.getenv('OPENSEARCH_PASSWORD'))
    )
    
    # Test with single stock
    symbol = "AAPL"  # Using Apple as test case
    period = "max"   # Get all historical data
    interval = "1d"  # Daily intervals
    
    try:
        print(f"Starting collection for {symbol}")
        print(f"Time: {datetime.now()}")
        print(f"Parameters: period={period}, interval={interval}")
        
        # Fetch data
        data = await collector.fetch_stock_data(symbol, period, interval)
        
        # Print data info
        print("\nData Overview:")
        print(f"Date Range: {data.index.min()} to {data.index.max()}")
        print(f"Number of records: {len(data)}")
        print("\nFirst few records:")
        print(data.head())
        
        # Store data
        result = await collector.collect_and_store(symbol, period)
        print("\nStorage Result:")
        print(result)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())