# services/data_collector/src/api/routers/stocks.py
from fastapi import APIRouter, HTTPException
from ...utils.collector import StockDataCollector

router = APIRouter()
collector = StockDataCollector()

@router.get("/{symbol}")
async def get_stock_data(symbol: str, period: str = "1d"):
    try:
        return await collector.get_stock_data(symbol, period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{symbol}/historical")
async def get_historical_data(
    symbol: str, 
    period: str = "1mo",  # 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    interval: str = "1d"  # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
):
    try:
        return await collector.get_historical_data(symbol, period, interval)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/info")
async def get_stock_info(symbol: str):
    try:
        return await collector.get_stock_info(symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))