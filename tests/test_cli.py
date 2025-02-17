"""CLI tests for image description functionality."""

import logging
import subprocess
from typing import Tuple

import pytest

logger = logging.getLogger(__name__)

# Test data
test_models = [
    pytest.param("gpt4", id="openai", marks=pytest.mark.openai),
    pytest.param("llama", id="llama", marks=pytest.mark.ollama),
    pytest.param(
        "claude",
        id="claude",
        marks=[
            pytest.mark.claude,
            pytest.mark.skip(reason="Claude not implemented yet"),
        ],
    ),
]

test_prompts = [
    pytest.param(None, id="default_prompt"),
    pytest.param(
        "List the main colors present in this image", id="color_prompt"
    ),
    pytest.param(
        "Describe the lighting and shadows", id="lighting_prompt"
    ),
]

error_cases = [
    ("nonexistent.jpg", "Image file not found"),
    (
        "test.txt",
        "Image file not found",
    ),  # CLI checks file existence before format
]


@pytest.mark.cli
class TestDescribeImageCLI:
    """Test suite for describe-image CLI."""

    @pytest.mark.parametrize("model", test_models)
    def test_model_specific(self, model: str, test_image_path: str):
        """Test CLI with different models."""
        cmd = [
            "describe-image",
            "-i",
            test_image_path,
            "-u",
            model,
            "-v",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode == 0
        ), f"CLI command failed with: {result.stderr}"
        assert len(result.stdout) > 100, "Description seems too short"

        # Model-specific output validation
        if model == "gpt4":
            assert any(
                term in result.stdout.lower()
                for term in ["scene", "image", "shows"]
            ), "GPT-4 output should be detailed and descriptive"
        elif model == "llama":
            assert any(
                term in result.stdout.lower()
                for term in ["forest", "tree", "nature"]
            ), "Llama output should identify nature elements"

    @pytest.mark.parametrize("prompt", test_prompts)
    @pytest.mark.parametrize("model", test_models)
    def test_prompts(
        self, prompt: str, model: str, test_image_path: str
    ):
        """Test CLI with different prompts and models."""
        cmd = ["describe-image", "-i", test_image_path, "-v"]
        if model:
            cmd.extend(["-u", model])
        if prompt:
            cmd.extend(["-p", prompt])

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode == 0
        ), f"CLI command failed with: {result.stderr}"

        # Prompt-specific validation
        if prompt and "color" in prompt.lower():
            assert any(
                term in result.stdout.lower()
                for term in ["color", "green", "brown"]
            ), "Custom color prompt was not reflected in output"
        elif prompt and "lighting" in prompt.lower():
            assert any(
                term in result.stdout.lower()
                for term in ["light", "shadow", "bright"]
            ), "Custom lighting prompt was not reflected in output"
        else:
            # Default prompt validation
            assert (
                len(result.stdout) > 100
            ), "Default prompt output seems too short"
            assert any(
                term in result.stdout.lower()
                for term in ["forest", "tree", "scene"]
            ), "Default prompt should describe the scene"

    @pytest.mark.parametrize("file_path,expected_error", error_cases)
    def test_error_cases(self, file_path: str, expected_error: str):
        """Test CLI error cases."""
        cmd = [
            "describe-image",
            "-i",
            file_path,
            "-v",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode != 0, "Command should fail"
        assert (
            expected_error in result.stderr
        ), f"Expected error message containing '{expected_error}'"

    def test_invalid_model(self, test_image_path: str):
        """Test CLI with invalid model."""
        cmd = [
            "describe-image",
            "-i",
            test_image_path,
            "-u",
            "invalid_model",
            "-v",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode != 0
        ), "Command should fail with invalid model"
        assert (
            "invalid choice: 'invalid_model'" in result.stderr
        ), "Expected invalid model error"

    @pytest.mark.parametrize("model", test_models)
    def test_verbose_output(self, model: str, test_image_path: str):
        """Test verbose output for different models."""
        # Test with verbose flag
        cmd_verbose = [
            "describe-image",
            "-i",
            test_image_path,
            "-u",
            model,
            "-v",
        ]
        result_verbose = subprocess.run(
            cmd_verbose, capture_output=True, text=True
        )

        # Test without verbose flag
        cmd_normal = [
            "describe-image",
            "-i",
            test_image_path,
            "-u",
            model,
        ]
        result_normal = subprocess.run(
            cmd_normal, capture_output=True, text=True
        )

        # Both should succeed
        assert result_verbose.returncode == 0, "Verbose command failed"
        assert result_normal.returncode == 0, "Normal command failed"

        # Both should provide descriptions
        assert (
            len(result_verbose.stdout) > 100
        ), "Verbose output seems too short"
        assert (
            len(result_normal.stdout) > 100
        ), "Normal output seems too short"

        # Verbose should show model registration
        assert (
            "Registering model type" in result_verbose.stderr
        ), "Verbose mode should show model registration"
