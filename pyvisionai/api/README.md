# PyVisionAI FastAPI

This module provides a RESTful API interface for PyVisionAI's image description capabilities.

## Running the API

```bash
# Install dependencies
poetry install

# Run the server
poetry run uvicorn pyvisionai.api.main:app --reload

# Or run on a specific port
poetry run uvicorn pyvisionai.api.main:app --reload --port 8080
```

## 📚 Interactive Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
  - Interactive API documentation
  - Try out endpoints directly in your browser
  - See all parameters with examples
  - Test file uploads

- **ReDoc**: http://localhost:8000/redoc
  - Alternative documentation format
  - Clean, readable interface

See [DOCUMENTATION.md](DOCUMENTATION.md) for a detailed guide on using the interactive docs.

## API Endpoints

### Image Description

- `POST /api/v1/describe/openai` - Describe image using OpenAI GPT-4 Vision
- `POST /api/v1/describe/ollama` - Describe image using Ollama (local)
- `POST /api/v1/describe/claude` - Describe image using Claude Vision
- `POST /api/v1/describe/auto` - Auto-select model with fallback
- `GET /api/v1/health` - Health check endpoint

### Parameters

All image description endpoints accept:
- `file`: Image file upload (multipart/form-data)
- `image_base64`: Base64 encoded image (for JSON requests)
- `api_key`: API key (optional, uses env var if not provided)
- `prompt`: Custom prompt (optional)
- `model`: Model variant (optional)
- `max_tokens`: Max response tokens (OpenAI/Claude only)

## Example Usage

### Using curl with file upload:
```bash
curl -X POST "http://localhost:8000/api/v1/describe/openai" \
  -F "file=@image.jpg" \
  -F "api_key=your-key" \
  -F "prompt=Describe this image"
```

### Using Python with base64:
```python
import base64
import requests

with open("image.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:8000/api/v1/describe/openai/json",
    json={
        "image_base64": image_base64,
        "api_key": "your-key",
        "prompt": "What's in this image?"
    }
)
print(response.json())
```

## Testing

Run the test suite:
```bash
poetry run pytest tests/test_fastapi_describe.py -v
```

## Environment Variables

- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic/Claude API key

## MCP (Model Context Protocol) Support 🤖

PyVisionAI now supports MCP, allowing AI agents like Claude Desktop to discover and use your image description tools directly!

See [MCP_SETUP.md](MCP_SETUP.md) for detailed setup instructions.

### Quick MCP Setup:

1. Start the server: `poetry run uvicorn pyvisionai.api.main:app --reload`
2. Configure Claude Desktop with your MCP server URL
3. Use natural language to analyze images through Claude

## Next Steps

Future enhancements will include:
- Document extraction endpoints
- Batch processing
- WebSocket support for real-time updates
- Authentication and rate limiting
