# services/data_collector/src/utils/logging.py
import logging
import watchtower
import boto3
from datetime import datetime

def setup_logging(service_name: str):
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    
    # CloudWatch handler
    cloudwatch_handler = watchtower.CloudWatchLogHandler(
        log_group=f'/stock-analysis/{service_name}',
        stream_name=datetime.now().strftime('%Y-%m-%d'),
        boto3_client=boto3.client('logs')
    )
    
    logger.addHandler(console_handler)
    logger.addHandler(cloudwatch_handler)
    
    return logger