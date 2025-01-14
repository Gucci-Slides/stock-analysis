# services/data_collector/tests/test_error_handling.py
import pytest
from src.utils.exceptions import retry_with_backoff, APIRateLimitError
import asyncio

@pytest.mark.asyncio
async def test_retry_mechanism():
    """Test retry decorator"""
    attempt_count = 0
    
    @retry_with_backoff(retries=3, backoff_in_seconds=0.1)
    async def failing_function():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise APIRateLimitError("Rate limit exceeded")
        return "success"
    
    result = await failing_function()
    assert result == "success"
    assert attempt_count == 3

@pytest.mark.asyncio
async def test_retry_max_attempts():
    """Test retry mechanism reaches max attempts"""
    @retry_with_backoff(retries=3, backoff_in_seconds=0.1)
    async def always_failing_function():
        raise APIRateLimitError("Rate limit exceeded")
    
    with pytest.raises(APIRateLimitError):
        await always_failing_function()