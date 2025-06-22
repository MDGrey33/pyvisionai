# PyVisionAI FastAPI - Curl Examples

## Image Description with OpenAI

### Option 1: Upload Image File (Recommended)
```bash
curl -X POST "http://localhost:8000/api/v1/describe/openai" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/image.jpg" \
  -F "api_key=your-openai-api-key" \
  -F "prompt=Describe this image in detail" \
  -F "max_tokens=500"
```

### Option 2: With Base64 Encoded Image
```bash
# First encode your image
base64 -i image.jpg -o image_base64.txt

# Then send the request
curl -X POST "http://localhost:8000/api/v1/describe/openai" \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "'$(cat image_base64.txt)'",
    "api_key": "your-openai-api-key",
    "model": "gpt-4o-mini",
    "prompt": "Describe this image in detail",
    "max_tokens": 300
  }'
```

### Response Example:
```json
{
  "description": "This image shows a modern office space with large windows overlooking a city skyline. There are several people working at computers...",
  "model_used": "gpt-4o-mini",
  "processing_time": 2.35
}
```

## Image Description with Ollama (Local)

```bash
curl -X POST "http://localhost:8000/api/v1/describe/ollama" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/image.jpg" \
  -F "model=llama3.2-vision:latest" \
  -F "prompt=What do you see in this image?"
```

## Image Description with Claude

```bash
curl -X POST "http://localhost:8000/api/v1/describe/claude" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/image.jpg" \
  -F "api_key=your-anthropic-api-key" \
  -F "prompt=Please describe this image" \
  -F "model=claude-3-opus-20240229" \
  -F "max_tokens=1024"
```

## Document Extraction

### Extract PDF with OpenAI
```bash
curl -X POST "http://localhost:8000/api/v1/extract/process" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf" \
  -F "file_type=pdf" \
  -F "extractor_type=page_as_image" \
  -F "model=gpt4" \
  -F "api_key=your-openai-api-key"
```

### Response:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "output_url": "/api/v1/download/550e8400-e29b-41d4-a716-446655440000/output.md",
  "status": "completed",
  "processing_time": 15.7
}
```

## Batch Processing

### Start Batch Job
```bash
curl -X POST "http://localhost:8000/api/v1/batch/process" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@document1.pdf" \
  -F "files=@document2.docx" \
  -F "files=@presentation.pptx" \
  -F "model=llama" \
  -F "max_workers=4"
```

### Check Batch Status
```bash
curl -X GET "http://localhost:8000/api/v1/batch/status/batch-id-here"
```

## Health Check

```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

Response:
```json
{
  "status": "healthy",
  "version": "0.3.1",
  "models_available": ["gpt4", "llama", "claude"]
}
```

## Using Environment Variables

Instead of passing API keys in requests, you can set them as environment variables:

```bash
# Set environment variables
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"

# Then make requests without api_key parameter
curl -X POST "http://localhost:8000/api/v1/describe/openai" \
  -F "file=@image.jpg"
```

## Error Response Example

```json
{
  "error": "Invalid API key",
  "detail": "The provided OpenAI API key is invalid or has insufficient permissions",
  "status_code": 401
}
