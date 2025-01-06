"""Configuration settings."""

import os

# Default settings
DEFAULT_PDF_EXTRACTOR = "page_as_image"
DEFAULT_IMAGE_MODEL = "gpt4"  # Default to GPT-4 for best results

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Directory structure
CONTENT_DIR = "./content"
SOURCE_DIR = os.path.join(CONTENT_DIR, "source")
EXTRACTED_DIR = os.path.join(CONTENT_DIR, "extracted")
LOG_DIR = os.path.join(CONTENT_DIR, "log")

# Create directories if they don't exist
for directory in [CONTENT_DIR, SOURCE_DIR, EXTRACTED_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True) 