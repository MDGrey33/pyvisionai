"""
Configuration file for the image description script.

This file contains the default configuration values used by the script.
You can modify these values to change the behavior of the script without
needing to modify the code.
"""

# The default path to the image file to be described.
# Replace this with the path to your desired image file.
DEFAULT_IMAGE_PATH = "./test_image.jpg"

# The default describer to use for generating image descriptions.
# Available options:
# - "openai": Use the OpenAI API for image description.
# - "ollama": Use the local ollama model for image description.
DEFAULT_DESCRIBER = "openai"

# The default model to use for image description.
# Available options:
# - OpenAI describer:
#   - "gpt-4o": The GPT-4 model optimized for image description (default).
#   - "gpt-3.5-turbo": The GPT-3.5 Turbo model.
# - ollama describer:
#   - "llava": The llava model.
#   - "llava:34b": The llava:34b model.
#   - "llama3.2-vision": The llama3.2-vision model.
DEFAULT_MODEL = "gpt-4o"

# The DOCX extraction method to use.
# Available options:
# - "text_and_images": Extract text and images separately.
#   This method preserves the original text formatting and extracts embedded images.
# - "page_as_image": Convert each page to an image.
#   This method captures the exact visual appearance of each page.
DEFAULT_DOCX_EXTRACTOR = "page_as_image"

# The PDF extraction method to use.
# Available options:
# - "text_and_images": Extract text and images separately.
#   This method preserves the original text formatting and extracts embedded images.
# - "page_as_image": Convert each page to an image.
#   This method captures the exact visual appearance of each page.
DEFAULT_PDF_EXTRACTOR = "page_as_image"
