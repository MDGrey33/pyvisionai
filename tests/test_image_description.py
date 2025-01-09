"""Tests for image description functionality."""

import os
import subprocess
import pytest
from pyvisionai import describe_image_ollama, describe_image_openai


def test_image_description_lib_gpt4(setup_test_env):
    """Test image description using GPT-4 through library API."""
    image_path = os.path.join("content", "test", "source", "test.jpeg")

    # Skip if no API key is provided
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("Skipping GPT-4 test - No API key provided")

    # Use GPT-4 Vision
    description = describe_image_openai(image_path, model="gpt-4o-mini")
    # Basic length check
    assert description and len(description) > 100, "Description seems too short"
    # Content verification
    assert any(
        term in description.lower() for term in ["forest", "tree"]
    ), "Expected forest scene description not found"


def test_image_description_cli_gpt4(setup_test_env):
    """Test image description using GPT-4 through CLI."""
    image_path = os.path.join("content", "test", "source", "test.jpeg")

    # Skip if no API key is provided
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("Skipping GPT-4 test - No API key provided")

    # Run CLI command
    cmd = [
        "describe-image",
        "-i",
        image_path,
        "-u",
        "gpt4",  # Use gpt4 use case
        "-k",
        api_key,
        "-v",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Verify output
    assert result.returncode == 0, f"CLI command failed with: {result.stderr}"
    assert len(result.stdout) > 100, "Description seems too short"
    # Content verification
    assert any(
        term in result.stdout.lower() for term in ["forest", "tree"]
    ), "Expected forest scene description not found"


def test_image_description_lib_llama(setup_test_env):
    """Test image description using Llama through library API."""
    image_path = os.path.join("content", "test", "source", "test.jpeg")

    # Use Llama model
    description = describe_image_ollama(image_path, model="llama3.2-vision")
    # Basic length check
    assert description and len(description) > 100, "Description seems too short"
    # Content verification
    assert any(
        term in description.lower() for term in ["forest", "tree"]
    ), "Expected forest scene description not found"


def test_image_description_cli_llama(setup_test_env):
    """Test image description using Llama through CLI."""
    image_path = os.path.join("content", "test", "source", "test.jpeg")

    # Run CLI command
    cmd = [
        "describe-image",
        "-i",
        image_path,
        "-u",
        "llama",  # Use llama use case
        "-v",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Verify output
    assert result.returncode == 0, f"CLI command failed with: {result.stderr}"
    assert len(result.stdout) > 100, "Description seems too short"
    # Content verification
    assert any(
        term in result.stdout.lower() for term in ["forest", "tree"]
    ), "Expected forest scene description not found"

