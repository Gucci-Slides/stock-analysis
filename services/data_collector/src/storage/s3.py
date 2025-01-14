# services/data_collector/src/storage/s3.py
import boto3
import json
from datetime import datetime
import pandas as pd
from io import StringIO

class S3Storage:
    def __init__(self, bucket_name: str):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name

    async def store_stock_data(self, symbol: str, data: pd.DataFrame):
        # Convert DataFrame to CSV
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=True)
        
        # Create S3 path with date partitioning
        today = datetime.now().strftime('%Y/%m/%d')
        s3_path = f'stock_data/{symbol}/{today}/{symbol}_data.csv'
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_path,
                Body=csv_buffer.getvalue()
            )
            return s3_path
        except Exception as e:
            raise Exception(f"Failed to store data in S3: {str(e)}")

    async def get_stock_data(self, symbol: str, date: str):
        s3_path = f'stock_data/{symbol}/{date}/{symbol}_data.csv'
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_path
            )
            df = pd.read_csv(StringIO(response['Body'].read().decode('utf-8')))
            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from S3: {str(e)}")