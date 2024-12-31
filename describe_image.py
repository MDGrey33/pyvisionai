"""
Generate descriptions for images using OpenAI's vision-capable models.
"""

import os
import argparse
from openai_describer import OpenAIDescriber
from typing import Optional

DEFAULT_IMAGE_PATH = "content/source/the_image.png"

def describe_image(
    image_path: str = DEFAULT_IMAGE_PATH, 
    model: str = "gpt-4o",
    api_key: Optional[str] = None,
) -> str:
    """
    Generate a description for an image using OpenAI's updated vision-capable model.

    Args:
        image_path (str): The path to the image file (default: content/source/the_image.png).
        model (str): The OpenAI model to use (default: "gpt-4o").
        api_key (str, optional): Your OpenAI API key. If None, it will use the OPENAI_API_KEY environment variable. 

    Returns:
        str: The description of the image.
    """
    describer = OpenAIDescriber(api_key=api_key)
    return describer.describe(image_path, model)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a description for an image using OpenAI API."
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
        "--model", type=str, default="gpt-4o", help="OpenAI model to use."
    )

    args = parser.parse_args()

    try:
        description = describe_image(
            args.image_path, model=args.model, api_key=args.api_key
        )
        print(f"Image Description:")
        print(description)
    except Exception as e:
        print(f"Error: {e}")
