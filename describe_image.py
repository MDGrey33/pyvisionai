"""
Generate descriptions for images using OpenAI's vision-capable models.
"""

import openai
import os
import base64
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
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "API key is required. Provide it as an argument or set it in the OPENAI_API_KEY environment variable."
        )

    openai.api_key = api_key
    client = openai.OpenAI()

    try:
        # Read and encode the image in base64
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": "Describe the image in extreme detail"}
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_data}"},
                        }
                    ],
                },
            ],
            response_format={"type": "text"},
            temperature=1,
            max_completion_tokens=10000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Print the response to inspect its structure
        print(response)

        # Access the content of the response correctly
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Failed to generate description: {e}")


if __name__ == "__main__":
    import argparse

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
