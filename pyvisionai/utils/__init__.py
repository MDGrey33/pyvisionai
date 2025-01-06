"""Utility functions and helpers."""

from .logger import logger, setup_logger
from .config import (
    DEFAULT_PDF_EXTRACTOR,
    DEFAULT_IMAGE_MODEL,
    OPENAI_API_KEY,
    OLLAMA_HOST,
    CONTENT_DIR,
    SOURCE_DIR,
    EXTRACTED_DIR,
    LOG_DIR,
)

__all__ = [
    "logger",
    "setup_logger",
    "DEFAULT_PDF_EXTRACTOR",
    "DEFAULT_IMAGE_MODEL",
    "OPENAI_API_KEY",
    "OLLAMA_HOST",
    "CONTENT_DIR",
    "SOURCE_DIR",
    "EXTRACTED_DIR",
    "LOG_DIR",
]
