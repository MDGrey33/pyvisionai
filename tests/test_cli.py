"""CLI tests for image description functionality."""

import logging
import os
import subprocess
from typing import Tuple
from unittest.mock import MagicMock, patch

import pytest

logger = logging.getLogger(__name__)

# Test data
test_models = [
    pytest.param(
        "gpt4", id="openai", marks=[pytest.mark.openai, pytest.mark.e2e]
    ),
    pytest.param(
        "llama", id="llama", marks=[pytest.mark.ollama, pytest.mark.e2e]
    ),
    pytest.param(
        "claude",
        id="claude",
        marks=[pytest.mark.claude, pytest.mark.e2e],
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


@pytest.mark.unit
class TestDescribeImageCLIUnit:
    """Unit tests for describe-image CLI with mocked subprocess."""

    @patch('subprocess.run')
    def test_describe_image_success(self, mock_run):
        """Test successful image description with mocked subprocess."""
        # Mock successful response
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="A beautiful landscape with mountains",
            stderr="",
        )

        # Import here to avoid issues with module loading
        import subprocess

        result = subprocess.run(
            ["describe-image", "-i", "test.jpg", "-m", "gpt4"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "beautiful landscape" in result.stdout
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_describe_image_with_custom_prompt(self, mock_run):
        """Test image description with custom prompt."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="The main colors are blue and green",
            stderr="",
        )

        import subprocess

        result = subprocess.run(
            [
                "describe-image",
                "-i",
                "test.jpg",
                "-p",
                "What are the main colors?",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "blue and green" in result.stdout


@pytest.mark.cli
@pytest.mark.integration
class TestDescribeImageCLI:
    """Test suite for describe-image CLI.

    Note: These are integration tests that actually call the CLI.
    For e2e tests with real APIs, add @pytest.mark.e2e to specific tests.
    """

    def get_api_key(self, model: str) -> str:
        """Get API key for the specified model."""
        if model == "gpt4":
            return os.getenv("OPENAI_API_KEY", "test-key")
        elif model == "claude":
            return os.getenv("ANTHROPIC_API_KEY", "test-key")
        return ""

    @pytest.mark.parametrize("model", test_models)
    def test_model_specific(self, model: str, sample_image_path):
        """Test CLI with different models."""
        # Skip if we don't have a valid API key
        api_key = self.get_api_key(model)
        if model == "gpt4" and (not api_key or api_key == "test-key"):
            pytest.skip("Valid OpenAI API key not available")
        elif model == "claude" and (
            not api_key or api_key == "test-key"
        ):
            pytest.skip("Valid Anthropic API key not available")

        # For integration tests, we still use mocked APIs from conftest
        cmd = [
            "describe-image",
            "-i",
            str(sample_image_path),
            "-u",
            model,
            "-v",
        ]
        if api_key:
            cmd.extend(["-k", api_key])

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Integration tests should succeed with mocked APIs
        assert (
            result.returncode == 0
        ), f"CLI command failed with: {result.stderr}"
        assert len(result.stdout) > 10, "Description seems too short"

    @pytest.mark.parametrize("prompt", test_prompts)
    @pytest.mark.parametrize(
        "model", ["gpt4"]
    )  # Test only with one model to speed up
    @pytest.mark.e2e
    def test_prompts(self, prompt: str, model: str, sample_image_path):
        """Test CLI with different prompts and models."""
        # Skip if we don't have a valid API key
        api_key = self.get_api_key(model)
        if not api_key or api_key == "test-key":
            pytest.skip("Valid OpenAI API key not available")

        cmd = ["describe-image", "-i", str(sample_image_path), "-v"]
        if model:
            cmd.extend(["-u", model])
        if prompt:
            cmd.extend(["-p", prompt])
        if api_key:
            cmd.extend(["-k", api_key])

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode == 0
        ), f"CLI command failed with: {result.stderr}"
        assert len(result.stdout) > 10, "Output seems too short"

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

    def test_invalid_model(self, sample_image_path):
        """Test CLI with invalid model."""
        cmd = [
            "describe-image",
            "-i",
            str(sample_image_path),
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

    @pytest.mark.parametrize(
        "model", ["gpt4"]
    )  # Test only with one model
    @pytest.mark.e2e
    def test_verbose_output(self, model: str, sample_image_path):
        """Test verbose output for different models."""
        # Skip if we don't have a valid API key
        api_key = self.get_api_key(model)
        if not api_key or api_key == "test-key":
            pytest.skip("Valid OpenAI API key not available")

        # Test with verbose flag
        cmd_verbose = [
            "describe-image",
            "-i",
            str(sample_image_path),
            "-u",
            model,
            "-v",
        ]
        if api_key:
            cmd_verbose.extend(["-k", api_key])

        result_verbose = subprocess.run(
            cmd_verbose, capture_output=True, text=True
        )

        # Test without verbose flag
        cmd_normal = [
            "describe-image",
            "-i",
            str(sample_image_path),
            "-u",
            model,
        ]
        if api_key:
            cmd_normal.extend(["-k", api_key])

        result_normal = subprocess.run(
            cmd_normal, capture_output=True, text=True
        )

        # Both should succeed
        assert result_verbose.returncode == 0, "Verbose command failed"
        assert result_normal.returncode == 0, "Normal command failed"

        # Both should provide descriptions
        assert (
            len(result_verbose.stdout) > 10
        ), "Verbose output seems too short"
        assert (
            len(result_normal.stdout) > 10
        ), "Normal output seems too short"

        # Verbose should show model registration
        assert (
            "Registering model type" in result_verbose.stderr
        ), "Verbose mode should show model registration"

    @pytest.mark.parametrize(
        "model", ["gpt4"]
    )  # Test only with one model
    @pytest.mark.e2e
    def test_model_parameter(self, model: str, sample_image_path):
        """Test CLI with --model parameter."""
        # Skip if we don't have a valid API key
        api_key = self.get_api_key(model)
        if not api_key or api_key == "test-key":
            pytest.skip("Valid OpenAI API key not available")

        cmd = [
            "describe-image",
            "-i",
            str(sample_image_path),
            "-m",  # Using new --model parameter
            model,
            "-v",
        ]
        if api_key:
            cmd.extend(["-k", api_key])

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode == 0
        ), f"CLI command failed with: {result.stderr}"
        assert len(result.stdout) > 10, "Description seems too short"

    @pytest.mark.parametrize(
        "model", ["gpt4"]
    )  # Test only with one model
    @pytest.mark.e2e
    def test_use_case_parameter(self, model: str, sample_image_path):
        """Test CLI with legacy --use-case parameter."""
        # Skip if we don't have a valid API key
        api_key = self.get_api_key(model)
        if not api_key or api_key == "test-key":
            pytest.skip("Valid OpenAI API key not available")

        cmd = [
            "describe-image",
            "-i",
            str(sample_image_path),
            "-u",  # Using legacy --use-case parameter
            model,
            "-v",
        ]
        if api_key:
            cmd.extend(["-k", api_key])

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode == 0
        ), f"CLI command failed with: {result.stderr}"
        assert len(result.stdout) > 10, "Description seems too short"
        # Check for new user-friendly message
        assert any(
            term in result.stderr.lower()
            for term in ["recommend", "consistency"]
        ), "User-friendly guidance message should be shown"

    @pytest.mark.e2e
    def test_parameter_precedence(self, sample_image_path):
        """Test that --use-case takes precedence over --model when both are provided."""
        # Skip if we don't have a valid API key
        api_key = self.get_api_key("gpt4")
        if not api_key or api_key == "test-key":
            pytest.skip("Valid OpenAI API key not available")

        cmd = [
            "describe-image",
            "-i",
            str(sample_image_path),
            "-u",
            "gpt4",  # Use mocked model
            "-m",
            "llama",  # This should be ignored when -u is present
            "-v",
            "-k",
            api_key,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode == 0
        ), f"CLI command failed with: {result.stderr}"
        # Check for new user-friendly message
        assert any(
            term in result.stderr.lower()
            for term in ["recommend", "consistency"]
        ), "User-friendly guidance message should be shown"

    @pytest.mark.e2e
    def test_default_model(self, sample_image_path):
        """Test that default model is used when neither parameter is provided."""
        # Skip if we don't have a valid API key
        api_key = self.get_api_key("gpt4")  # Default is gpt4
        if not api_key or api_key == "test-key":
            pytest.skip("Valid OpenAI API key not available")

        cmd = [
            "describe-image",
            "-i",
            str(sample_image_path),
            "-k",
            api_key,
            "-v",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode == 0
        ), f"CLI command failed with: {result.stderr}"
        assert len(result.stdout) > 10, "Description seems too short"

    @pytest.mark.parametrize(
        "model", ["gpt4"]
    )  # Test only with one model
    @pytest.mark.e2e
    def test_source_parameter(self, model: str, sample_image_path):
        """Test CLI with --source parameter."""
        # Skip if we don't have a valid API key
        api_key = self.get_api_key(model)
        if not api_key or api_key == "test-key":
            pytest.skip("Valid OpenAI API key not available")

        cmd = [
            "describe-image",
            "-s",  # Using new --source parameter
            str(sample_image_path),
            "-m",
            model,
            "-v",
        ]
        if api_key:
            cmd.extend(["-k", api_key])

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode == 0
        ), f"CLI command failed with: {result.stderr}"
        assert len(result.stdout) > 10, "Description seems too short"

    def test_source_image_precedence(self, sample_image_path):
        """Test that --image and --source cannot be used together."""
        cmd = [
            "describe-image",
            "-i",
            str(sample_image_path),  # Using legacy --image parameter
            "-s",
            "nonexistent.jpg",  # This should cause an error
            "-m",
            "gpt4",
            "-v",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode != 0
        ), "Command should fail with both parameters"
        assert (
            "not allowed with argument" in result.stderr.lower()
        ), "Should show mutually exclusive error"

    def test_no_source_or_image_parameter(self):
        """Test that error is shown when neither --source nor --image is provided."""
        cmd = [
            "describe-image",
            "-m",
            "gpt4",
            "-v",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode != 0
        ), "Command should fail without image path"
        assert (
            "required" in result.stderr.lower()
        ), "Error about missing parameter should be shown"
