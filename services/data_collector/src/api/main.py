# services/data_collector/src/api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import stocks
from ..utils.logging import logger
from ..utils.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router, prefix="/api/v1/stocks", tags=["stocks"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up stock data collector service")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down stock data collector service")

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": settings.app_name,
        "endpoints": {
            "stock_data": "/api/v1/stocks/{symbol}",
            "stock_info": "/api/v1/stocks/{symbol}/info"
        }
    }