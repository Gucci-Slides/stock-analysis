# tests/test_collector.py
import pytest
from src.collectors.stock_collector import StockDataCollector

@pytest.fixture
def stock_collector():
    return StockDataCollector(
        s3_bucket='test-bucket',
        opensearch_endpoint='test-endpoint',
        opensearch_auth=('admin', 'password')
    )

def test_stock_data_collector(stock_collector):
    assert stock_collector is not None
    assert stock_collector.s3_bucket == 'test-bucket'