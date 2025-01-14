# src/api/health.py
from fastapi import APIRouter, Request
from typing import Dict
import psutil
import time

router = APIRouter()

def check_s3_connection(s3_client) -> bool:
    try:
        s3_client.list_buckets()
        return True
    except Exception:
        return False

def check_opensearch_connection(os_client) -> bool:
    try:
        return os_client.ping()
    except Exception:
        return False

@router.get("/health")
async def health_check(request: Request) -> Dict:
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "s3": "healthy",
            "opensearch": "healthy"
        },
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }
    }
    
    # Check S3
    if not check_s3_connection(request.app.state.s3_client):
        health_status["services"]["s3"] = "unhealthy"
        health_status["status"] = "degraded"
    
    # Check OpenSearch
    if not check_opensearch_connection(request.app.state.os_client):
        health_status["services"]["opensearch"] = "unhealthy"
        health_status["status"] = "degraded"
    
    return health_status