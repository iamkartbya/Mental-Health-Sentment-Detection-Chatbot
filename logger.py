"""
Logging configuration for Milo AI application.
Provides structured logging throughout the application.
"""

import logging
import sys
from typing import Optional
from config import CONFIG


# Configure logging format
_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str) -> logging.Logger:
    """
    Setup and return a configured logger instance.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(CONFIG.log_level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(CONFIG.log_level)
    
    formatter = logging.Formatter(_LOG_FORMAT, _DATE_FORMAT)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


# Module-level logger
logger = setup_logger(__name__)
