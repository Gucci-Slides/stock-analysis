# services/data_collector/tests/conftest.py
import pytest
import pandas as pd
from datetime import datetime, timedelta
import boto3
from moto import mock_aws
from opensearchpy import OpenSearch

@pytest.fixture
def sample_stock_data():
    """Create sample stock data for testing"""
    dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='D')
    data = {
        'Open': [100.0] * len(dates),
        'High': [105.0] * len(dates),
        'Low': [95.0] * len(dates),
        'Close': [102.0] * len(dates),
        'Volume': [1000000] * len(dates)
    }
    return pd.DataFrame(data, index=dates)

@pytest.fixture
def invalid_stock_data():
    """Create invalid stock data for testing"""
    dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='D')
    data = {
        'Open': [100.0] * len(dates),
        'High': [90.0] * len(dates),  # High less than Low (invalid)
        'Low': [95.0] * len(dates),
        'Close': [102.0] * len(dates),
        'Volume': [-1000] * len(dates)  # Negative volume (invalid)
    }
    return pd.DataFrame(data, index=dates)

@pytest.fixture
def mock_s3_client():
    """Create mock S3 client"""
    with mock_aws():
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket='test-bucket')
        yield s3

@pytest.fixture
def mock_opensearch_client():
    """Create mock OpenSearch client"""
    return OpenSearch(
        hosts=[{'host': 'localhost', 'port': 9200}],
        http_auth=('admin', 'admin'),
        use_ssl=False,
    )