# services/data_collector/src/utils/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Add these to existing settings
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket_name: str
    elasticsearch_hosts: list
    
    class Config:
        env_file = ".env"
    app_name: str = "Stock Data Collector"
    debug: bool = False
    redis_url: str = "redis://localhost:6379"
    cache_ttl: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()