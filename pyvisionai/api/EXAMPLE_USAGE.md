# PyVisionAI API - Example Usage

## Quick Start

### 1. Start the API server

```bash
poetry run uvicorn pyvisionai.api.main:app --reload
```

### 2. Visit the Interactive Docs

Open http://localhost:8000/docs in your browser

### 3. Try an Endpoint

#### Example: OpenAI Image Description

1. Click on `POST /api/v1/describe/openai`
2. Click "Try it out"
3. **IMPORTANT**: Replace the default values:
   - Click "Choose File" and select an image
   - **api_key**: Enter your actual OpenAI API key (or set `OPENAI_API_KEY` environment variable)
   - **model**: Leave as `gpt-4o-mini` or change to `gpt-4o` for better quality
   - **prompt**: Optional - customize what you want to know about the image
   - **max_tokens**: Leave as 300 or increase for longer descriptions

4. Click "Execute"

## Common Mistakes to Avoid

### ❌ Don't leave "string" in form fields
The Swagger UI shows "string" as a data type indicator, not as the actual value to use.

### ❌ Don't use "test-key" as API key
You need a real API key from OpenAI, Anthropic, or have Ollama running locally.

### ✅ Valid Model Names

**OpenAI Models:**
- `gpt-4o-mini` (default, fast and cheap)
- `gpt-4o` (best quality)
- `gpt-4-vision-preview`
- `gpt-4-turbo`

**Ollama Models:**
- `llama3.2-vision:latest` (default)
- `llava:latest`
- `bakllava:latest`

**Claude Models:**
- `claude-3-opus-20240229` (default)
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307`

## Example with cURL

### Correct Usage
```bash
# With API key in environment
export OPENAI_API_KEY="sk-your-actual-key"
curl -X POST "http://localhost:8000/api/v1/describe/openai" \
  -F "file=@myimage.jpg" \
  -F "model=gpt-4o-mini"

# With API key in request
curl -X POST "http://localhost:8000/api/v1/describe/openai" \
  -F "file=@myimage.jpg" \
  -F "api_key=sk-your-actual-key" \
  -F "model=gpt-4o-mini" \
  -F "prompt=What objects are in this image?"
```

## Python Example

```python
import requests

# Correct usage
response = requests.post(
    "http://localhost:8000/api/v1/describe/openai",
    files={"file": open("image.jpg", "rb")},
    data={
        "api_key": "sk-your-actual-key",  # Real API key
        "model": "gpt-4o-mini",           # Valid model name
        "prompt": "Describe this image",
        "max_tokens": 500
    }
)

print(response.json())
```

## Response Format

Success (200 OK):
```json
{
  "description": "This image shows a golden retriever sitting on a green lawn...",
  "model_used": "gpt-4o-mini",
  "processing_time": 1.23
}
```

Error (422 Validation Error):
```json
{
  "detail": "Please provide a valid model name. Valid options: gpt-4o, gpt-4o-mini, gpt-4-vision-preview, gpt-4-turbo"
}
```

Error (401 Unauthorized):
```json
{
  "detail": "Error code: 401 - {'error': {'message': 'Incorrect API key provided...'}}"
}
```
