"""FastAPI application for PyVisionAI."""

import base64
import io
import os
import tempfile
import time
from enum import Enum
from typing import Optional

from fastapi import Body, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel, Field

from pyvisionai import (
    describe_image,
    describe_image_claude,
    describe_image_ollama,
    describe_image_openai,
)
from pyvisionai.utils.config import DEFAULT_PROMPT


class OpenAIModel(str, Enum):
    """Available OpenAI vision models."""

    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_VISION_PREVIEW = "gpt-4-vision-preview"
    GPT_4_TURBO = "gpt-4-turbo"


class OllamaModel(str, Enum):
    """Common Ollama vision models."""

    LLAMA32_VISION = "llama3.2-vision:latest"
    LLAVA = "llava:latest"
    BAKLLAVA = "bakllava:latest"


app = FastAPI(
    title="PyVisionAI API",
    description="""
    🚀 **PyVisionAI API** - AI-powered image description and document extraction

    This API provides endpoints for describing images using various AI models including:
    - OpenAI GPT-4 Vision
    - Ollama (local models)
    - Claude Vision
    - Auto-selection with fallback

    ## Features
    - 📤 File upload support
    - 🔤 Base64 image support
    - 🎯 Custom prompts
    - 🔄 Automatic model fallback
    - 🔑 Environment variable support for API keys
    """,
    version="0.3.1",
    docs_url="/docs",
    redoc_url="/redoc",
)


class ImageDescriptionRequest(BaseModel):
    """Request model for image description with base64."""

    image_base64: str = Field(
        ...,
        description="Base64 encoded image data",
        example="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
    )
    model: Optional[str] = Field(
        None,
        description="Model to use for description",
        example="gpt-4o",
    )
    api_key: Optional[str] = Field(
        None,
        description="API key for the service (uses environment variable if not provided)",
        example="sk-...",
    )
    prompt: Optional[str] = Field(
        None,
        description="Custom prompt for image description",
        example="Describe this image in detail",
    )
    max_tokens: Optional[int] = Field(
        300, description="Maximum tokens in response", example=500
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                    "prompt": "What do you see in this image?",
                    "model": "gpt-4o-mini",
                    "max_tokens": 300,
                }
            ]
        }
    }


class ImageDescriptionResponse(BaseModel):
    """Response model for image description."""

    description: str = Field(
        ...,
        description="AI-generated description of the image",
        example="This image shows a beautiful sunset over the ocean with orange and purple hues in the sky.",
    )
    model_used: str = Field(
        ...,
        description="The model that was used for description",
        example="gpt-4o-mini",
    )
    processing_time: float = Field(
        ...,
        description="Time taken to process the request in seconds",
        example=1.23,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "description": "This image shows a red square on a white background. The square appears to be perfectly centered and has clean, sharp edges.",
                    "model_used": "gpt-4o-mini",
                    "processing_time": 1.45,
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str
    detail: Optional[str] = None
    status_code: int


def save_uploaded_file(
    file_content: bytes, suffix: str = ".jpg"
) -> str:
    """Save uploaded file to a temporary location."""
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=suffix
    ) as tmp_file:
        tmp_file.write(file_content)
        return tmp_file.name


def decode_base64_image(image_base64: str) -> bytes:
    """Decode base64 image data."""
    try:
        # Remove data URL prefix if present
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]
        return base64.b64decode(image_base64)
    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Invalid base64 data: {str(e)}"
        )


@app.post(
    "/api/v1/describe/openai",
    response_model=ImageDescriptionResponse,
    operation_id="describe_image_with_openai",
    summary="Describe image using OpenAI GPT-4 Vision - Use this tool to analyze and describe images using OpenAI's vision models",
    description="Use OpenAI's GPT-4 Vision models to describe an uploaded image or base64 encoded image",
    tags=["Image Description"],
    responses={
        200: {
            "description": "Successfully described the image",
            "content": {
                "application/json": {
                    "example": {
                        "description": "A serene landscape with mountains in the background and a lake in the foreground reflecting the sunset.",
                        "model_used": "gpt-4o-mini",
                        "processing_time": 2.34,
                    }
                }
            },
        },
        422: {
            "description": "Validation error - missing image or invalid data"
        },
        500: {"description": "Internal server error or API error"},
    },
)
async def describe_image_openai_endpoint(
    file: Optional[UploadFile] = File(
        None,
        description="Image file to describe (JPEG, PNG, GIF, WebP supported)",
    ),
    api_key: Optional[str] = Form(
        None,
        description="OpenAI API key (uses OPENAI_API_KEY env var if not provided)",
    ),
    model: Optional[str] = Form(
        "gpt-4o-mini",
        description="OpenAI model to use (defaults to gpt-4o-mini)",
        example="gpt-4o-mini",
    ),
    prompt: Optional[str] = Form(
        "Describe this image in detail",
        description="Custom prompt for image description (optional)",
        example="Describe this image focusing on colors and composition",
    ),
    max_tokens: Optional[int] = Form(
        300, description="Maximum tokens in response", example=500
    ),
):
    """
    Describe an image using OpenAI's GPT-4 Vision model.

    You can upload an image file using multipart/form-data.
    For base64 images, use the /api/v1/describe/openai/json endpoint.

    The API key can be provided in the request or set as OPENAI_API_KEY environment variable.
    """
    start_time = time.time()

    # Handle image input
    if not file:
        raise HTTPException(
            status_code=422,
            detail="File must be provided. For base64 images, use /api/v1/describe/openai/json",
        )

    image_content = await file.read()
    image_path = save_uploaded_file(image_content, suffix=".jpg")

    try:
        # Use environment variable if API key not provided
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")

        # Validate model name
        valid_models = [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-vision-preview",
            "gpt-4-turbo",
        ]
        if model and model.lower() == "string":
            raise HTTPException(
                status_code=422,
                detail="Please provide a valid model name. Valid options: "
                + ", ".join(valid_models),
            )

        description = describe_image_openai(
            image_path=image_path,
            model=model,
            api_key=api_key,
            max_tokens=max_tokens,
            prompt=prompt or DEFAULT_PROMPT,
        )

        processing_time = time.time() - start_time

        return ImageDescriptionResponse(
            description=description,
            model_used=model or "gpt-4o-mini",
            processing_time=processing_time,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if 'image_path' in locals():
            try:
                os.unlink(image_path)
            except Exception:
                pass


@app.post(
    "/api/v1/describe/ollama",
    response_model=ImageDescriptionResponse,
    operation_id="describe_image_with_ollama",
    summary="Describe image using local Ollama models - Use this tool for private/local image analysis without sending data to external APIs",
    description="Use local Ollama models to describe an image (requires Ollama running locally)",
    tags=["Image Description"],
)
async def describe_image_ollama_endpoint(
    file: Optional[UploadFile] = File(
        None, description="Image file to describe"
    ),
    model: Optional[str] = Form(
        "llama3.2-vision:latest",
        description="Ollama model to use (defaults to llama3.2-vision:latest)",
        example="llama3.2-vision:latest",
    ),
    prompt: Optional[str] = Form(
        None, description="Custom prompt", example="Describe this image"
    ),
):
    """Describe an image using Ollama's local vision model."""
    start_time = time.time()

    # Handle image input
    if not file:
        raise HTTPException(
            status_code=422, detail="File must be provided"
        )

    image_content = await file.read()
    image_path = save_uploaded_file(image_content)

    try:
        description = describe_image_ollama(
            image_path=image_path,
            model=model,
            prompt=prompt or DEFAULT_PROMPT,
        )

        processing_time = time.time() - start_time

        return ImageDescriptionResponse(
            description=description,
            model_used=model or "llama3.2-vision:latest",
            processing_time=processing_time,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if 'image_path' in locals():
            try:
                os.unlink(image_path)
            except Exception:
                pass


@app.post(
    "/api/v1/describe/claude",
    response_model=ImageDescriptionResponse,
    operation_id="describe_image_with_claude",
    summary="Describe image using Claude Vision - Use this tool for detailed image analysis with Anthropic's Claude",
    description="Use Anthropic's Claude Vision to describe an image",
    tags=["Image Description"],
)
async def describe_image_claude_endpoint(
    file: Optional[UploadFile] = File(
        None, description="Image file to describe"
    ),
    api_key: Optional[str] = Form(
        None,
        description="Anthropic API key (uses ANTHROPIC_API_KEY env var if not provided)",
    ),
    model: Optional[str] = Form(
        "claude-3-opus-20240229", description="Claude model to use"
    ),
    prompt: Optional[str] = Form(None, description="Custom prompt"),
    max_tokens: Optional[int] = Form(
        1024, description="Maximum tokens in response"
    ),
):
    """Describe an image using Claude Vision."""
    start_time = time.time()

    # Handle image input
    if not file:
        raise HTTPException(
            status_code=422, detail="File must be provided"
        )

    image_content = await file.read()
    image_path = save_uploaded_file(image_content)

    try:
        # Use environment variable if API key not provided
        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")

        # Note: Current Claude implementation doesn't support model/max_tokens params
        # but we accept them for future compatibility
        description = describe_image_claude(
            image_path=image_path,
            api_key=api_key,
            prompt=prompt or DEFAULT_PROMPT,
        )

        processing_time = time.time() - start_time

        return ImageDescriptionResponse(
            description=description,
            model_used=model,
            processing_time=processing_time,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if 'image_path' in locals():
            try:
                os.unlink(image_path)
            except Exception:
                pass


@app.post(
    "/api/v1/describe/auto",
    response_model=ImageDescriptionResponse,
    operation_id="describe_image_auto",
    summary="Auto-select best available model - Use this tool when you want the system to automatically choose the best vision model",
    description="Automatically selects the best available model with fallback support",
    tags=["Image Description"],
)
async def describe_image_auto_endpoint(
    file: Optional[UploadFile] = File(
        None, description="Image file to describe"
    ),
    model: Optional[str] = Form(
        None,
        description="Preferred model (will fallback if not available)",
    ),
    prompt: Optional[str] = Form(None, description="Custom prompt"),
):
    """Describe an image using automatic model selection with fallback."""
    start_time = time.time()

    # Handle image input
    if not file:
        raise HTTPException(
            status_code=422, detail="File must be provided"
        )

    image_content = await file.read()
    image_path = save_uploaded_file(image_content)

    try:
        # Use the base describe_image function with automatic fallback
        # Note: Current implementation doesn't support prompt parameter
        # We'll need to enhance the base function to support it
        description = describe_image(
            image_path=image_path,
            model=model,
        )

        processing_time = time.time() - start_time

        # Try to determine which model was actually used
        # This is a simplified approach - in production we'd track this properly
        model_used = model or "auto-selected"

        return ImageDescriptionResponse(
            description=description,
            model_used=model_used,
            processing_time=processing_time,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if 'image_path' in locals():
            try:
                os.unlink(image_path)
            except Exception:
                pass


@app.get(
    "/api/v1/health",
    summary="Health check",
    description="Check API health and available models",
    tags=["System"],
)
async def health_check():
    """
    Check the health status of the API.

    Returns information about:
    - API status
    - Version
    - Available models
    """
    # Check which models are available
    models_available = []

    # Check OpenAI
    if os.getenv("OPENAI_API_KEY"):
        models_available.append("openai")

    # Check Ollama (simplified check)
    try:
        import requests

        response = requests.get(
            "http://localhost:11434/api/tags", timeout=1
        )
        if response.status_code == 200:
            models_available.append("ollama")
    except Exception:
        pass

    # Check Claude
    if os.getenv("ANTHROPIC_API_KEY"):
        models_available.append("claude")

    return {
        "status": "healthy",
        "version": "0.3.1",
        "models_available": models_available,
        "endpoints": {
            "image_description": [
                "/api/v1/describe/openai",
                "/api/v1/describe/ollama",
                "/api/v1/describe/claude",
                "/api/v1/describe/auto",
            ],
            "documentation": ["/docs", "/redoc"],
        },
    }


# Support JSON requests as well
@app.post(
    "/api/v1/describe/openai/json",
    response_model=ImageDescriptionResponse,
    summary="Describe image using OpenAI (JSON)",
    description="JSON endpoint for OpenAI image description",
    tags=["Image Description"],
)
async def describe_image_openai_json(request: ImageDescriptionRequest):
    """
    Describe an image using OpenAI (JSON request).

    This endpoint accepts a JSON body with base64 encoded image data.
    """
    start_time = time.time()

    # Decode base64 image
    image_content = decode_base64_image(request.image_base64)
    image_path = save_uploaded_file(image_content)

    try:
        # Use environment variable if API key not provided
        api_key = request.api_key
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")

        description = describe_image_openai(
            image_path=image_path,
            model=request.model,
            api_key=api_key,
            max_tokens=request.max_tokens or 300,
            prompt=request.prompt or DEFAULT_PROMPT,
        )

        processing_time = time.time() - start_time

        return ImageDescriptionResponse(
            description=description,
            model_used=request.model or "gpt-4o-mini",
            processing_time=processing_time,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if 'image_path' in locals():
            try:
                os.unlink(image_path)
            except Exception:
                pass


@app.get("/", include_in_schema=False)
async def root():
    """Redirect to documentation."""
    return {
        "message": "Welcome to PyVisionAI API",
        "documentation": "/docs",
        "alternative_docs": "/redoc",
        "health": "/api/v1/health",
    }


# Initialize MCP server
mcp = FastApiMCP(
    app,
    name="PyVisionAI MCP Server",
    description="AI-powered image description service with support for OpenAI, Claude, and Ollama models",
)

# Mount MCP server
mcp.mount()
