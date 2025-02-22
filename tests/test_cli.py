"""CLI tests for image description functionality."""

import logging
import os
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
        marks=pytest.mark.claude,
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

    def get_api_key(self, model: str) -> str:
        """Get API key for the specified model."""
        if model == "gpt4":
            return os.getenv("OPENAI_API_KEY", "")
        elif model == "claude":
            return os.getenv("ANTHROPIC_API_KEY", "")
        return ""

    @pytest.mark.parametrize("model", test_models)
    def test_model_specific(self, model: str, test_image_path: str):
        """Test CLI with different models."""
        # Skip if required API key is missing
        api_key = self.get_api_key(model)
        if model in ["gpt4", "claude"] and not api_key:
            pytest.skip(f"Skipping {model} test - No API key provided")

        cmd = [
            "describe-image",
            "-i",
            test_image_path,
            "-u",
            model,
            "-v",
        ]
        if api_key:
            cmd.extend(["-k", api_key])

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
        # Skip if required API key is missing
        api_key = self.get_api_key(model)
        if model in ["gpt4", "claude"] and not api_key:
            pytest.skip(f"Skipping {model} test - No API key provided")

        cmd = ["describe-image", "-i", test_image_path, "-v"]
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
        # Skip if required API key is missing
        api_key = self.get_api_key(model)
        if model in ["gpt4", "claude"] and not api_key:
            pytest.skip(f"Skipping {model} test - No API key provided")

        # Test with verbose flag
        cmd_verbose = [
            "describe-image",
            "-i",
            test_image_path,
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
            test_image_path,
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
            len(result_verbose.stdout) > 100
        ), "Verbose output seems too short"
        assert (
            len(result_normal.stdout) > 100
        ), "Normal output seems too short"

        # Verbose should show model registration
        assert (
            "Registering model type" in result_verbose.stderr
        ), "Verbose mode should show model registration"

    @pytest.mark.parametrize("model", test_models)
    def test_model_parameter(self, model: str, test_image_path: str):
        """Test CLI with --model parameter."""
        # Skip if required API key is missing
        api_key = self.get_api_key(model)
        if model in ["gpt4", "claude"] and not api_key:
            pytest.skip(f"Skipping {model} test - No API key provided")

        cmd = [
            "describe-image",
            "-i",
            test_image_path,
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

    @pytest.mark.parametrize("model", test_models)
    def test_use_case_parameter(self, model: str, test_image_path: str):
        """Test CLI with legacy --use-case parameter."""
        # Skip if required API key is missing
        api_key = self.get_api_key(model)
        if model in ["gpt4", "claude"] and not api_key:
            pytest.skip(f"Skipping {model} test - No API key provided")

        cmd = [
            "describe-image",
            "-i",
            test_image_path,
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
        assert len(result.stdout) > 100, "Description seems too short"
        # Check for new user-friendly message
        assert all(
            term in result.stderr.lower()
            for term in ["recommend", "consistency"]
        ), "User-friendly guidance message should be shown"

    def test_parameter_precedence(self, test_image_path: str):
        """Test that --use-case takes precedence over --model when both are provided."""
        cmd = [
            "describe-image",
            "-i",
            test_image_path,
            "-u",
            "llama",  # Using local model to avoid API key requirement
            "-m",
            "gpt4",  # This should be ignored when -u is present
            "-v",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode == 0
        ), f"CLI command failed with: {result.stderr}"
        # Check that llama-specific output is present (indicating -u took precedence)
        assert any(
            term in result.stdout.lower()
            for term in ["forest", "tree", "nature"]
        ), "Use case parameter should take precedence"
        # Check for new user-friendly message
        assert all(
            term in result.stderr.lower()
            for term in ["recommend", "consistency"]
        ), "User-friendly guidance message should be shown"

    def test_default_model(self, test_image_path: str):
        """Test that default model is used when neither parameter is provided."""
        # Skip if required API key is missing (assuming default is gpt4)
        api_key = self.get_api_key("gpt4")
        if not api_key:
            pytest.skip("Skipping test - No OpenAI API key provided")

        cmd = [
            "describe-image",
            "-i",
            test_image_path,
            "-k",
            api_key,
            "-v",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode == 0
        ), f"CLI command failed with: {result.stderr}"
        assert len(result.stdout) > 100, "Description seems too short"
        # Verify GPT-4 specific output (as it's the default)
        assert any(
            term in result.stdout.lower()
            for term in ["scene", "image", "shows"]
        ), "Default model (GPT-4) output should be detailed and descriptive"

    @pytest.mark.parametrize("model", test_models)
    def test_source_parameter(self, model: str, test_image_path: str):
        """Test CLI with --source parameter."""
        # Skip if required API key is missing
        api_key = self.get_api_key(model)
        if model in ["gpt4", "claude"] and not api_key:
            pytest.skip(f"Skipping {model} test - No API key provided")

        cmd = [
            "describe-image",
            "-s",  # Using new --source parameter
            test_image_path,
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
        assert len(result.stdout) > 100, "Description seems too short"

    def test_source_image_precedence(self, test_image_path: str):
        """Test that --image and --source cannot be used together."""
        cmd = [
            "describe-image",
            "-i",
            test_image_path,  # Using legacy --image parameter
            "-s",
            "nonexistent.jpg",  # This should cause an error
            "-m",
            "llama",  # Using local model to avoid API key requirement
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
            "llama",  # Using local model to avoid API key requirement
            "-v",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        assert (
            result.returncode != 0
        ), "Command should fail without image path"
        assert (
            "required" in result.stderr.lower()
        ), "Error about missing parameter should be shown"
