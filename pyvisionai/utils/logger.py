"""Logging configuration for the pyvisionai package."""

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(
    name: str = "pyvisionai", log_dir: str | Path | None = None
) -> logging.Logger:
    """
    Set up a logger with file and console handlers.

    Args:
        name: Name for the logger (default: pyvisionai)
        log_dir: Directory for log files (optional)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatters
    console_formatter = logging.Formatter("%(message)s")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (if log_dir is provided)
    if log_dir is not None:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{name.replace('.', '_')}.log"
        file_handler = logging.FileHandler(str(log_file))
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


# Create the default logger instance
logger = setup_logger()
