"""
Generate descriptions for images using OpenAI's vision-capable models or the ollama model.
"""

import os
from typing import Optional
import config
from openai_describer import OpenAIDescriber
from ollama_describer import OllamaDescriber

def create_describer(describer_choice: str, api_key: Optional[str] = None, model: str = config.DEFAULT_MODEL):
    if describer_choice == "openai":
        return OpenAIDescriber(api_key=api_key)
    elif describer_choice == "ollama":
        return OllamaDescriber(model=model)
    else:
        raise ValueError(f"Invalid describer choice: {describer_choice}")

def describe_image(
    image_path: str = config.DEFAULT_IMAGE_PATH,
    model: str = config.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    describer_choice: str = config.DEFAULT_DESCRIBER,
) -> str:
    """
    Generate a description for an image using the specified describer.

    Args:
        image_path (str): The path to the image file (default: config.DEFAULT_IMAGE_PATH).
        model (str): The model to use for image description (default: config.DEFAULT_MODEL).
        api_key (str, optional): Your OpenAI API key. If None, it will use the OPENAI_API_KEY environment variable.
        describer_choice (str): The describer to use (default: config.DEFAULT_DESCRIBER). Can be "openai" or "ollama".

    Returns:
        str: The description of the image.
    """
    describer = create_describer(describer_choice, api_key, model)
    return describer.describe(image_path)

if __name__ == "__main__":
    try:
        description = describe_image()
        print(f"Image Description:")
        print(description)
    except Exception as e:
        print(f"Error: {e}")
