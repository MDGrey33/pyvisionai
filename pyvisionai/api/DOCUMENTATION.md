# PyVisionAI API Interactive Documentation

FastAPI automatically generates beautiful, interactive API documentation for you!

## Accessing the Documentation

When you run the API server, you can access the documentation at:

### 1. **Swagger UI** (Interactive Docs)
- URL: `http://localhost:8000/docs`
- Features:
  - 🎯 Try out API endpoints directly from your browser
  - 📋 See all parameters with descriptions and examples
  - 🔄 Test file uploads interactively
  - 📝 View request/response schemas
  - 🎨 Beautiful, modern interface

### 2. **ReDoc** (Alternative Documentation)
- URL: `http://localhost:8000/redoc`
- Features:
  - 📖 Clean, readable documentation
  - 🔍 Search functionality
  - 📱 Mobile-friendly
  - 🖨️ Print-friendly format

## What You'll See

### In the Swagger UI (`/docs`):

1. **API Overview**
   - Title: "PyVisionAI API"
   - Description with features and capabilities
   - Version information

2. **Endpoints Grouped by Tags**
   - **Image Description** endpoints:
     - POST `/api/v1/describe/openai`
     - POST `/api/v1/describe/ollama`
     - POST `/api/v1/describe/claude`
     - POST `/api/v1/describe/auto`
     - POST `/api/v1/describe/openai/json`
   - **System** endpoints:
     - GET `/api/v1/health`

3. **For Each Endpoint You Can**:
   - Click to expand and see full details
   - View all parameters with:
     - Names and types
     - Descriptions
     - Example values
     - Whether they're required or optional
   - Click "Try it out" button
   - Upload files or enter data
   - Click "Execute" to test the endpoint
   - See the actual curl command
   - View the response with status code and body

4. **Example Values**
   - Pre-filled example data for testing
   - Sample base64 images
   - Example prompts
   - Response examples showing what to expect

## Quick Start

1. **Start the API server**:
   ```bash
   poetry run uvicorn pyvisionai.api.main:app --reload
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:8000/docs
   ```

3. **Try the OpenAI endpoint**:
   - Click on `POST /api/v1/describe/openai`
   - Click "Try it out"
   - Click "Choose File" and select an image
   - Enter your API key (or set it as environment variable)
   - Optionally modify the prompt
   - Click "Execute"
   - See the AI-generated description!

## Example Screenshots (What You'll See)

### Main Documentation Page
```
PyVisionAI API
🚀 PyVisionAI API - AI-powered image description and document extraction

This API provides endpoints for describing images using various AI models including:
- OpenAI GPT-4 Vision
- Ollama (local models)
- Claude Vision
- Auto-selection with fallback

Features
- 📤 File upload support
- 🔤 Base64 image support
- 🎯 Custom prompts
- 🔄 Automatic model fallback
- 🔑 Environment variable support for API keys

[Image Description]
  POST /api/v1/describe/openai    Describe image using OpenAI
  POST /api/v1/describe/ollama    Describe image using Ollama
  POST /api/v1/describe/claude    Describe image using Claude
  POST /api/v1/describe/auto      Auto-select model for image description

[System]
  GET /api/v1/health              Health check
```

### Endpoint Detail View
```
POST /api/v1/describe/openai
Describe image using OpenAI

Use OpenAI's GPT-4 Vision models to describe an uploaded image or base64 encoded image

Parameters:
- file*         [Choose File]    Image file to describe (JPEG, PNG, GIF, WebP supported)
- image_base64  [________]       Base64 encoded image (alternative to file upload)
- api_key       [________]       OpenAI API key (uses OPENAI_API_KEY env var if not provided)
- model         [gpt-4o-mini]    OpenAI model to use
- prompt        [________]       Custom prompt for image description
- max_tokens    [500]           Maximum tokens in response

[Try it out] [Execute]

Responses:
200 Successfully described the image
{
  "description": "A serene landscape with mountains in the background...",
  "model_used": "gpt-4o-mini",
  "processing_time": 2.34
}
```

## Tips

1. **Environment Variables**: Set your API keys as environment variables to avoid entering them each time:
   ```bash
   export OPENAI_API_KEY="your-key"
   export ANTHROPIC_API_KEY="your-key"
   ```

2. **File Uploads**: The interactive docs support drag-and-drop for file uploads

3. **Copy Examples**: Click on example values to copy them to the input fields

4. **Export**: You can export the API specification as OpenAPI/Swagger JSON from the docs

5. **Authentication**: If you add authentication later, the docs will show a lock icon and allow you to authenticate

## For Developers

The documentation is automatically generated from:
- Function docstrings
- Pydantic model definitions
- FastAPI decorators
- Type hints

This means the documentation is always up-to-date with your code!
