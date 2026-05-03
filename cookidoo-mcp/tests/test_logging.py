import logging
from src.logging_config import logger

def test_logger_created():
    assert logger is not None
    assert isinstance(logger, logging.Logger)
    assert logger.name == "cookidoo-mcp"
