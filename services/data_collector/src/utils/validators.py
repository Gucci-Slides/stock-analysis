# services/data_collector/src/utils/validators.py
import pandas as pd
from .exceptions import ValidationError

def validate_stock_data(data: pd.DataFrame) -> bool:
    """Validate stock data before storage"""
    try:
        # Check if DataFrame is empty
        if data.empty:
            raise ValidationError("Empty dataset received")
            
        # Check for required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in data.columns for col in required_columns):
            raise ValidationError(f"Missing required columns. Required: {required_columns}")
            
        # Check for null values
        if data[required_columns].isnull().any().any():
            raise ValidationError("Dataset contains null values")
            
        # Check data types
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(data[col]):
                raise ValidationError(f"Column {col} is not numeric")
                
        # Check for logical consistency
        if not (data['High'] >= data['Low']).all():
            raise ValidationError("High price is lower than Low price")
            
        # Check for future dates
        if (data.index > pd.Timestamp.now()).any():
            raise ValidationError("Dataset contains future dates")
            
        return True
        
    except Exception as e:
        raise ValidationError(f"Validation failed: {str(e)}")