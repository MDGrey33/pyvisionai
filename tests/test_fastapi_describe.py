"""Tests for FastAPI image description endpoints."""

import base64
import io
import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from PIL import Image

# We'll import the app once it's created
# from pyvisionai.api.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    from pyvisionai.api.main import app

    return TestClient(app)


@pytest.fixture
def test_image_bytes():
    """Create a test image in memory."""
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()


@pytest.fixture
def test_image_base64(test_image_bytes):
    """Create a base64 encoded test image."""
    return base64.b64encode(test_image_bytes).decode()


class TestDescribeImageEndpoints:
    """Test suite for image description endpoints."""

    @pytest.mark.parametrize(
        "endpoint",
        [
            "/api/v1/describe/openai",
            "/api/v1/describe/ollama",
            "/api/v1/describe/claude",
            "/api/v1/describe/auto",
        ],
    )
    def test_endpoint_exists(self, client, endpoint):
        """Test that all image description endpoints exist."""
        response = client.post(endpoint)
        # Should return 422 (validation error) not 404
        assert response.status_code != 404

    def test_openai_with_file_upload(self, client, test_image_bytes):
        """Test OpenAI endpoint with file upload."""
        with patch(
            'pyvisionai.api.main.describe_image_openai'
        ) as mock_describe:
            mock_describe.return_value = "A red square image"

            response = client.post(
                "/api/v1/describe/openai",
                files={
                    "file": ("test.jpg", test_image_bytes, "image/jpeg")
                },
                data={
                    "api_key": "test-key",
                    "prompt": "Describe this image",
                    "model": "gpt-4-vision-preview",
                    "max_tokens": "500",
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["description"] == "A red square image"
            assert data["model_used"] == "gpt-4-vision-preview"
            assert "processing_time" in data

            # Verify the function was called with correct parameters
            mock_describe.assert_called_once()
            call_args = mock_describe.call_args[1]
            assert call_args["api_key"] == "test-key"
            assert call_args["prompt"] == "Describe this image"
            assert call_args["model"] == "gpt-4-vision-preview"
            assert call_args["max_tokens"] == 500

    def test_openai_with_base64(self, client, test_image_base64):
        """Test OpenAI endpoint with base64 encoded image."""
        with patch(
            'pyvisionai.api.main.describe_image_openai'
        ) as mock_describe:
            mock_describe.return_value = "A red square image"

            # Use the JSON endpoint for base64
            response = client.post(
                "/api/v1/describe/openai/json",
                json={
                    "image_base64": test_image_base64,
                    "api_key": "test-key",
                    "prompt": "What do you see?",
                    "max_tokens": 300,
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["description"] == "A red square image"
            assert "processing_time" in data

    def test_ollama_with_file_upload(self, client, test_image_bytes):
        """Test Ollama endpoint with file upload."""
        with patch(
            'pyvisionai.api.main.describe_image_ollama'
        ) as mock_describe:
            mock_describe.return_value = "Local description of image"

            response = client.post(
                "/api/v1/describe/ollama",
                files={
                    "file": ("test.jpg", test_image_bytes, "image/jpeg")
                },
                data={
                    "model": "llama3.2-vision:latest",
                    "prompt": "Describe this image",
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["description"] == "Local description of image"
            assert data["model_used"] == "llama3.2-vision:latest"

    def test_claude_with_file_upload(self, client, test_image_bytes):
        """Test Claude endpoint with file upload."""
        with patch(
            'pyvisionai.api.main.describe_image_claude'
        ) as mock_describe:
            mock_describe.return_value = "Claude's description"

            response = client.post(
                "/api/v1/describe/claude",
                files={
                    "file": ("test.jpg", test_image_bytes, "image/jpeg")
                },
                data={
                    "api_key": "test-claude-key",
                    "prompt": "Analyze this image",
                    "model": "claude-3-opus-20240229",
                    "max_tokens": "1024",
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["description"] == "Claude's description"
            assert data["model_used"] == "claude-3-opus-20240229"

    def test_auto_describe_with_file(self, client, test_image_bytes):
        """Test auto-select endpoint."""
        with patch(
            'pyvisionai.api.main.describe_image'
        ) as mock_describe:
            mock_describe.return_value = "Auto-selected description"

            response = client.post(
                "/api/v1/describe/auto",
                files={
                    "file": ("test.jpg", test_image_bytes, "image/jpeg")
                },
                data={"prompt": "What's in this image?"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["description"] == "Auto-selected description"
            assert "model_used" in data

    def test_missing_file_and_base64(self, client):
        """Test error when neither file nor base64 is provided."""
        response = client.post(
            "/api/v1/describe/openai", data={"api_key": "test-key"}
        )

        assert response.status_code == 422
        assert "File must be provided" in response.text

    def test_invalid_base64(self, client):
        """Test error with invalid base64 data."""
        # Use the JSON endpoint
        response = client.post(
            "/api/v1/describe/openai/json",
            json={
                "image_base64": "invalid-base64-data",
                "api_key": "test-key",
            },
        )

        assert response.status_code == 422
        assert "Invalid base64" in response.text

    def test_api_error_handling(self, client, test_image_bytes):
        """Test API error handling."""
        with patch(
            'pyvisionai.api.main.describe_image_openai'
        ) as mock_describe:
            mock_describe.side_effect = Exception(
                "API Error: Invalid key"
            )

            response = client.post(
                "/api/v1/describe/openai",
                files={
                    "file": ("test.jpg", test_image_bytes, "image/jpeg")
                },
                data={"api_key": "invalid-key"},
            )

            assert response.status_code == 500
            data = response.json()
            assert "API Error" in data["detail"]

    def test_default_parameters(self, client, test_image_bytes):
        """Test that default parameters are applied correctly."""
        with patch(
            'pyvisionai.api.main.describe_image_openai'
        ) as mock_describe:
            mock_describe.return_value = "Description with defaults"

            response = client.post(
                "/api/v1/describe/openai",
                files={
                    "file": ("test.jpg", test_image_bytes, "image/jpeg")
                },
            )

            assert response.status_code == 200

            # Check defaults were used
            call_args = mock_describe.call_args[1]
            assert (
                call_args["model"] is None
                or call_args["model"] == "gpt-4o-mini"
            )
            assert call_args["max_tokens"] == 300

    def test_environment_api_key(self, client, test_image_bytes):
        """Test using API key from environment."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"}):
            with patch(
                'pyvisionai.api.main.describe_image_openai'
            ) as mock_describe:
                mock_describe.return_value = "Description"

                response = client.post(
                    "/api/v1/describe/openai",
                    files={
                        "file": (
                            "test.jpg",
                            test_image_bytes,
                            "image/jpeg",
                        )
                    },
                )

                assert response.status_code == 200
                # FastAPI should pass the env key to the function
                call_args = mock_describe.call_args[1]
                assert (
                    call_args["api_key"] == "env-key"
                )  # FastAPI reads env and passes it

    @pytest.mark.parametrize(
        "file_type",
        ["image/jpeg", "image/png", "image/gif", "image/webp"],
    )
    def test_supported_image_formats(self, client, file_type):
        """Test different image format support."""
        # Create appropriate image based on format
        img = Image.new('RGB', (100, 100), color='blue')
        img_byte_arr = io.BytesIO()

        format_map = {
            "image/jpeg": "JPEG",
            "image/png": "PNG",
            "image/gif": "GIF",
            "image/webp": "WEBP",
        }
        img.save(img_byte_arr, format=format_map[file_type])
        img_byte_arr.seek(0)

        with patch(
            'pyvisionai.api.main.describe_image_openai'
        ) as mock_describe:
            mock_describe.return_value = f"Image in {file_type} format"

            response = client.post(
                "/api/v1/describe/openai",
                files={
                    "file": (
                        "test.img",
                        img_byte_arr.getvalue(),
                        file_type,
                    )
                },
                data={"api_key": "test-key"},
            )

            assert response.status_code == 200


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "models_available" in data
        assert isinstance(data["models_available"], list)
