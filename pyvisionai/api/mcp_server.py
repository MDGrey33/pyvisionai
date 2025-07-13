"""MCP Server for PyVisionAI - Exposes image description capabilities as MCP tools."""

import base64
import os
import tempfile
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

from pyvisionai import (
    describe_image_claude,
    describe_image_ollama,
    describe_image_openai,
)
from pyvisionai.utils.config import DEFAULT_PROMPT

# Create MCP server instance
mcp = FastMCP("pyvisionai")


def save_base64_image(image_base64: str) -> str:
    """Save base64 image to temporary file and return path."""
    try:
        # Remove data URL prefix if present
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]

        image_data = base64.b64decode(image_base64)

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".jpg"
        ) as tmp_file:
            tmp_file.write(image_data)
            return tmp_file.name
    except Exception as e:
        raise ValueError(f"Invalid base64 image data: {str(e)}")


@mcp.tool()
def describe_image_with_openai(
    image_path: str,
    model: str = "gpt-4o",
    prompt: Optional[str] = None,
    max_tokens: int = 300,
) -> str:
    """
    Describe an image using OpenAI's GPT-4 Vision models.

    Args:
        image_path: Path to the image file or base64 encoded image data
        model: OpenAI model to use (gpt-4o, gpt-4o-mini, gpt-4-vision-preview)
        prompt: Custom prompt for description (optional)
        max_tokens: Maximum tokens in response

    Returns:
        Description of the image
    """
    try:
        # Check if input is base64 or file path
        if image_path.startswith("data:") or len(image_path) > 500:
            # Likely base64 data
            actual_path = save_base64_image(image_path)
            cleanup = True
        else:
            actual_path = image_path
            cleanup = False

        # Verify file exists
        if not os.path.exists(actual_path):
            return f"Error: Image file not found at {actual_path}"

        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "Error: OPENAI_API_KEY environment variable not set"

        # Call the describe function
        description = describe_image_openai(
            image_path=actual_path,
            model=model,
            api_key=api_key,
            max_tokens=max_tokens,
            prompt=prompt or DEFAULT_PROMPT,
        )

        # Cleanup temp file if needed
        if cleanup:
            try:
                os.unlink(actual_path)
            except Exception:
                pass

        return description

    except Exception as e:
        return f"Error describing image with OpenAI: {str(e)}"


@mcp.tool()
def describe_image_with_ollama(
    image_path: str,
    model: str = "llama3.2-vision:latest",
    prompt: Optional[str] = None,
) -> str:
    """
    Describe an image using local Ollama vision models.

    Args:
        image_path: Path to the image file or base64 encoded image data
        model: Ollama model to use (llama3.2-vision:latest, llava:latest, etc.)
        prompt: Custom prompt for description (optional)

    Returns:
        Description of the image
    """
    try:
        # Check if input is base64 or file path
        if image_path.startswith("data:") or len(image_path) > 500:
            # Likely base64 data
            actual_path = save_base64_image(image_path)
            cleanup = True
        else:
            actual_path = image_path
            cleanup = False

        # Verify file exists
        if not os.path.exists(actual_path):
            return f"Error: Image file not found at {actual_path}"

        # Call the describe function
        description = describe_image_ollama(
            image_path=actual_path,
            model=model,
            prompt=prompt or DEFAULT_PROMPT,
        )

        # Cleanup temp file if needed
        if cleanup:
            try:
                os.unlink(actual_path)
            except Exception:
                pass

        return description

    except Exception as e:
        return f"Error describing image with Ollama: {str(e)}"


@mcp.tool()
def describe_image_with_claude(
    image_path: str, prompt: Optional[str] = None
) -> str:
    """
    Describe an image using Anthropic's Claude Vision.

    Args:
        image_path: Path to the image file or base64 encoded image data
        prompt: Custom prompt for description (optional)

    Returns:
        Description of the image
    """
    try:
        # Check if input is base64 or file path
        if image_path.startswith("data:") or len(image_path) > 500:
            # Likely base64 data
            actual_path = save_base64_image(image_path)
            cleanup = True
        else:
            actual_path = image_path
            cleanup = False

        # Verify file exists
        if not os.path.exists(actual_path):
            return f"Error: Image file not found at {actual_path}"

        # Get API key from environment
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return (
                "Error: ANTHROPIC_API_KEY environment variable not set"
            )

        # Call the describe function
        description = describe_image_claude(
            image_path=actual_path,
            api_key=api_key,
            prompt=prompt or DEFAULT_PROMPT,
        )

        # Cleanup temp file if needed
        if cleanup:
            try:
                os.unlink(actual_path)
            except Exception:
                pass

        return description

    except Exception as e:
        return f"Error describing image with Claude: {str(e)}"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
