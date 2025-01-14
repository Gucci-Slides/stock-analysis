# services/data_collector/src/models/stock.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class StockData(BaseModel):
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    
class StockDataResponse(BaseModel):
    symbol: str
    data: List[StockData]
    last_updated: datetime

class DataCollectionRequest(BaseModel):
    symbol: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    interval: str = "1d"