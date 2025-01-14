# services/data_collector/tests/test_logging.py
import pytest
from src.utils.logging import setup_logging
import logging

def test_logger_setup():
    """Test logger configuration"""
    logger = setup_logging('test-service')
    assert logger.name == 'test-service'
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 2  # Console and CloudWatch handlers

def test_logger_messages(caplog):
    """Test logger message handling"""
    logger = setup_logging('test-service')
    with caplog.at_level(logging.INFO):
        logger.info("Test message")
        assert "Test message" in caplog.text