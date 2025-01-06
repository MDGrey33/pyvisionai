"""Image description using OpenAI's GPT-4 Vision model."""

import base64
from typing import Optional
from openai import OpenAI

from ..utils.logger import logger


def describe_image_openai(
    image_path: str,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    max_tokens: int = 300
) -> str:
    """
    Describe an image using OpenAI's GPT-4 Vision model.

    Args:
        image_path: Path to the image file
        model: Name of the OpenAI model to use
        api_key: OpenAI API key (optional if set in environment)
        max_tokens: Maximum tokens in the response

    Returns:
        str: Description of the image
    """
    try:
        # Initialize client
        client = OpenAI(api_key=api_key)

        # Read and encode image
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode()

        # Prepare request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this image in detail."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=max_tokens
        )

        # Extract description
        description = response.choices[0].message.content.strip()

        if not description:
            raise ValueError("No description generated")

        return description

    except Exception as e:
        logger.error(f"Error describing image with OpenAI: {str(e)}")
        raise 