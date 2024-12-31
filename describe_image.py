"""
Generate descriptions for images using OpenAI's vision-capable models or the ollama model.
"""

import os
import argparse
from openai_describer import OpenAIDescriber
from ollama_describer import OllamaDescriber
from typing import Optional

DEFAULT_IMAGE_PATH = "content/source/the_image.png"

def create_describer(describer_choice: str, api_key: Optional[str] = None):
    if describer_choice == "openai":
        return OpenAIDescriber(api_key=api_key)
    elif describer_choice == "ollama":
        return OllamaDescriber()
    else:
        raise ValueError(f"Invalid describer choice: {describer_choice}")

def describe_image(
    image_path: str = DEFAULT_IMAGE_PATH,
    model: str = "gpt-4o",
    api_key: Optional[str] = None,
    describer_choice: str = "openai",
) -> str:
    """
    Generate a description for an image using the specified describer.

    Args:
        image_path (str): The path to the image file (default: content/source/the_image.png).
        model (str): The OpenAI model to use (default: "gpt-4o"). Only applicable for the OpenAI describer.
        api_key (str, optional): Your OpenAI API key. If None, it will use the OPENAI_API_KEY environment variable.
        describer_choice (str): The describer to use (default: "openai"). Can be "openai" or "ollama".

    Returns:
        str: The description of the image.
    """
    describer = create_describer(describer_choice, api_key)
    return describer.describe(image_path, model) if describer_choice == "openai" else describer.describe(image_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a description for an image using OpenAI API or ollama model."
    )
    parser.add_argument(
        "--image_path",
        type=str,
        default=DEFAULT_IMAGE_PATH,
        help="Path to the image file.",
    )
    parser.add_argument(
        "--api_key", type=str, default=None, help="OpenAI API key (optional)."
    )
    parser.add_argument(
        "--model", type=str, default="gpt-4o", help="OpenAI model to use (only applicable for OpenAI describer)."
    )
    parser.add_argument(
        "--describer", type=str, default="openai", choices=["openai", "ollama"], help="Describer to use (openai or ollama)."
    )

    args = parser.parse_args()

    try:
        description = describe_image(
            args.image_path, model=args.model, api_key=args.api_key, describer_choice=args.describer
        )
        print(f"Image Description:")
        print(description)
    except Exception as e:
        print(f"Error: {e}")
