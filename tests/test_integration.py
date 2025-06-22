"""Integration tests for image description functionality."""

import logging

import pytest

from pyvisionai import describe_image_ollama, describe_image_openai

logger = logging.getLogger(__name__)


@pytest.mark.integration
@pytest.mark.e2e
class TestImageDescription:
    """Integration tests for image description."""

    @pytest.mark.openai
    @pytest.mark.e2e
    def test_openai_description(self, sample_image_path):
        """Test OpenAI image description."""
        description = describe_image_openai(sample_image_path)
        assert len(description) > 100, "Description seems too short"
        assert any(
            term in description.lower() for term in ["forest", "tree"]
        ), "Expected forest scene description not found"

    @pytest.mark.ollama
    @pytest.mark.e2e
    def test_ollama_description(self, sample_image_path):
        """Test Ollama image description."""
        description = describe_image_ollama(sample_image_path)
        assert len(description) > 100, "Description seems too short"
        assert any(
            term in description.lower() for term in ["forest", "tree"]
        ), "Expected forest scene description not found"

    @pytest.mark.openai
    @pytest.mark.e2e
    def test_openai_custom_prompt(self, sample_image_path):
        """Test OpenAI with custom prompt."""
        custom_prompt = "List the main colors present in this image"
        description = describe_image_openai(
            sample_image_path,
            prompt=custom_prompt,
        )
        assert any(
            term in description.lower()
            for term in ["color", "green", "brown"]
        ), "Custom prompt was not reflected in output"

    @pytest.mark.ollama
    @pytest.mark.e2e
    def test_ollama_custom_prompt(self, sample_image_path):
        """Test Ollama with custom prompt."""
        custom_prompt = "List the main colors present in this image"
        description = describe_image_ollama(
            sample_image_path,
            prompt=custom_prompt,
        )
        assert any(
            term in description.lower()
            for term in ["color", "green", "brown"]
        ), "Custom prompt was not reflected in output"
