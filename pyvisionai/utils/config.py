"""Configuration constants for PyVisionAI."""

import os

# Default directories
CONTENT_DIR = "content"
SOURCE_DIR = os.path.join(CONTENT_DIR, "source")
EXTRACTED_DIR = os.path.join(CONTENT_DIR, "extracted")
LOG_DIR = os.path.join(CONTENT_DIR, "log")

# Default settings
DEFAULT_IMAGE_MODEL = "gpt4"  # Default to GPT-4 for best results
DEFAULT_PDF_EXTRACTOR = "page_as_image"  # or "text_and_images"

# Model names
OLLAMA_MODEL_NAME = "llama3.2-vision"  # Default Ollama model
OPENAI_MODEL_NAME = "gpt-4o-mini"  # Default OpenAI model

# Default prompts for image description
DEFAULT_PROMPT = (
    "Describe this image in detail. Preserve as much of the precise "
    "original text, format, images and style as possible."
)

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Create directories if they don't exist
for directory in [CONTENT_DIR, SOURCE_DIR, EXTRACTED_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)
