# services/data_collector/tests/test_validators.py
import pytest
from src.utils.validators import validate_stock_data
from src.utils.exceptions import ValidationError
from datetime import datetime, timedelta
import pandas as pd

def test_valid_stock_data(sample_stock_data):
    """Test validation with valid stock data"""
    assert validate_stock_data(sample_stock_data) is True

def test_invalid_stock_data(invalid_stock_data):
    """Test validation with invalid stock data"""
    with pytest.raises(ValidationError):
        validate_stock_data(invalid_stock_data)

def test_missing_columns():
    """Test validation with missing columns"""
    data = pd.DataFrame({
        'Open': [100.0],
        'Close': [102.0]  # Missing High, Low, Volume
    })
    with pytest.raises(ValidationError, match="Missing required columns"):
        validate_stock_data(data)

def test_future_dates():
    """Test validation with future dates"""
    future_date = datetime.now() + timedelta(days=1)
    data = pd.DataFrame({
        'Open': [100.0],
        'High': [105.0],
        'Low': [95.0],
        'Close': [102.0],
        'Volume': [1000000]
    }, index=[future_date])
    
    with pytest.raises(ValidationError, match="contains future dates"):
        validate_stock_data(data)