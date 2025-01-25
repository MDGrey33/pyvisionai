"""Utility functions and helpers."""

from .config import (
    CONTENT_DIR,
    DEFAULT_IMAGE_MODEL,
    DEFAULT_PDF_EXTRACTOR,
    EXTRACTED_DIR,
    LOG_DIR,
    OLLAMA_HOST,
    OPENAI_API_KEY,
    SOURCE_DIR,
)
from .logger import logger, setup_logger
from .retry import (
    APIError,
    ConnectionError,
    RateLimitError,
    RetryableError,
    RetryManager,
    RetryStrategy,
    TemporaryError,
)

__all__ = [
    "logger",
    "setup_logger",
    "RetryManager",
    "RetryStrategy",
    "RetryableError",
    "APIError",
    "RateLimitError",
    "TemporaryError",
    "ConnectionError",
    "DEFAULT_PDF_EXTRACTOR",
    "DEFAULT_IMAGE_MODEL",
    "OPENAI_API_KEY",
    "OLLAMA_HOST",
    "CONTENT_DIR",
    "SOURCE_DIR",
    "EXTRACTED_DIR",
    "LOG_DIR",
]
