"""
Logging configuration for the file extractor application.
"""

import os
import logging
from datetime import datetime

def setup_logger():
    """Configure and set up the logger for the application."""
    # Create logs directory if it doesn't exist
    log_dir = "content/log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"file_extractor_{timestamp}.log")
    
    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create a logger instance
    logger = logging.getLogger('file_extractor')
    logger.setLevel(logging.INFO)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Prevent logging from propagating to the root logger
    logger.propagate = False
    
    return logger

# Create and configure the logger
logger = setup_logger() 