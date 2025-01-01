"""
Configuration file for the image description script.

This file contains the default configuration values used by the script.
You can modify these values to change the behavior of the script without
needing to modify the code in describe_image.py.
"""

# The default path to the image file to be described.
# Replace this with the path to your desired image file.
DEFAULT_IMAGE_PATH = "content/source/the_image.png"

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
DEFAULT_MODEL = "gpt-3.5-turbo"
