"""Command-line interface for image description."""

import os
import argparse
from typing import Optional

from file_extractor.describers import describe_image_ollama, describe_image_openai
from file_extractor.utils.logger import logger


# Available models for each service
OLLAMA_MODEL = "llama3.2-vision"
GPT4_MODEL = "gpt-4o-mini"


def describe_image_cli(
    image_path: str,
    model: str = "llama",
    api_key: Optional[str] = None,
    verbose: bool = False
) -> str:
    """
    Describe an image using the specified model.

    Args:
        image_path: Path to the image file
        model: Model to use (llama, gpt3, or gpt4)
        api_key: OpenAI API key (required for gpt3/gpt4)
        verbose: Whether to print verbose output

    Returns:
        str: Description of the image

    Note:
        - llama: Uses Ollama's llama3.2-vision model (local)
        - gpt3/gpt4: Uses OpenAI's gpt-4o-mini model (cloud)
    """
    try:
        # Validate image path
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Set OpenAI API key if provided
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        # Get description based on model
        if model == "llama":
            description = describe_image_ollama(image_path, model=OLLAMA_MODEL)
        elif model in ["gpt3", "gpt4"]:
            # Both GPT-3 and GPT-4 use cases use the same vision model
            description = describe_image_openai(image_path, model=GPT4_MODEL)
        else:
            raise ValueError(f"Unsupported model: {model}")

        if verbose:
            print(f"\nDescription:\n{description}\n")

        return description

    except Exception as e:
        if verbose:
            logger.error(f"\nError: {str(e)}")
        raise


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Describe an image using various models.")
    parser.add_argument("-i", "--image", required=True, help="Path to the image file")
    parser.add_argument(
        "-u", "--use-case",
        choices=["llama", "gpt3", "gpt4"],
        default="llama",
        help="Model to use for description"
    )
    parser.add_argument(
        "-k", "--api-key",
        help="OpenAI API key (required for GPT models)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print verbose output"
    )

    args = parser.parse_args()

    try:
        description = describe_image_cli(
            args.image,
            args.use_case,
            args.api_key,
            args.verbose
        )
        print(description)
    except Exception as e:
        logger.error(str(e))
        exit(1)


if __name__ == "__main__":
    main() 