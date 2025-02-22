"""Command-line interface for image description."""

import argparse
import os
from typing import Optional

from pyvisionai.describers import (
    describe_image_claude,
    describe_image_ollama,
    describe_image_openai,
)
from pyvisionai.utils.config import DEFAULT_IMAGE_MODEL, DEFAULT_PROMPT
from pyvisionai.utils.logger import logger


def describe_image_cli(
    image_path: str,
    model: str = DEFAULT_IMAGE_MODEL,
    api_key: Optional[str] = None,
    verbose: bool = False,
    prompt: Optional[str] = None,
) -> str:
    """
    Describe an image using the specified model.

    Args:
        image_path: Path to the image file
        model: Model to use (llama, gpt3, gpt4, or claude)
        api_key: API key (required for gpt3/gpt4/claude)
        verbose: Whether to print verbose output
        prompt: Custom prompt for image description (optional)

    Returns:
        str: Description of the image

    Note:
        - llama: Uses Ollama's llama3.2-vision model (local)
        - gpt3/gpt4: Uses OpenAI's gpt-4o-mini model (cloud)
        - claude: Uses Anthropic's Claude 3 Opus model (cloud)
    """
    try:
        # Validate image path
        if not os.path.exists(image_path):
            raise FileNotFoundError(
                f"Image file not found: {image_path}"
            )

        # Get description based on model
        if model == "llama":
            description = describe_image_ollama(
                image_path,
                prompt=prompt,
            )
        elif model in ["gpt3", "gpt4"]:
            # Set OpenAI API key if provided
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
            # Both GPT-3 and GPT-4 use cases use the same vision model
            description = describe_image_openai(
                image_path,
                api_key=api_key,
                prompt=prompt,
            )
        elif model == "claude":
            # Set Anthropic API key if provided
            if api_key:
                os.environ["ANTHROPIC_API_KEY"] = api_key
            description = describe_image_claude(
                image_path,
                api_key=api_key,
                prompt=prompt,
            )
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
    parser = argparse.ArgumentParser(
        description="Describe an image using various models."
    )

    # Source parameter group
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "-s",
        "--source",
        help="Path to the image file to describe",
    )
    source_group.add_argument(
        "-i",
        "--image",
        help="[Legacy] Path to the image file. For consistency with other commands, we recommend using -s/--source instead.",
    )

    parser.add_argument(
        "-u",
        "--use-case",
        choices=["llama", "gpt3", "gpt4", "claude"],
        help="Legacy parameter for model selection. We recommend using --model for consistency, though --use-case remains supported for backward compatibility.",
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=["llama", "gpt3", "gpt4", "claude"],
        default=DEFAULT_IMAGE_MODEL,
        help="Model to use for description (gpt4: GPT-4 Vision, claude: Claude Vision, llama: Local Llama)",
    )
    parser.add_argument(
        "-k",
        "--api-key",
        help="API key (required for GPT and Claude models)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose output",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        help=f"Custom prompt for image description (default: {DEFAULT_PROMPT})",
    )

    args = parser.parse_args()

    try:
        # Determine which parameter was used and set image_path
        if args.image:
            image_path = args.image
            logger.warning(
                "For better consistency across commands, we recommend using -s/--source instead of -i/--image. "
                "Both parameters remain fully supported for backward compatibility."
            )
        else:
            image_path = args.source

        # Handle model parameter precedence
        model = (
            args.use_case if args.use_case is not None else args.model
        )
        if args.use_case is not None:
            logger.warning(
                "For better consistency across commands, we recommend using -m/--model instead of -u/--use-case. "
                "Both parameters remain fully supported for backward compatibility."
            )

        description = describe_image_cli(
            image_path,
            model,
            args.api_key,
            args.verbose,
            args.prompt,
        )
        print(description)
    except Exception as e:
        logger.error(str(e))
        exit(1)


if __name__ == "__main__":
    main()
