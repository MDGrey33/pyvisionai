# Swagger UI Tips for PyVisionAI API

## Fixed: Separate Endpoints for Different Input Types

The API now clearly separates file upload endpoints from JSON endpoints to avoid confusion in Swagger UI.

### For File Uploads (Multipart Form Data)

Use these endpoints for uploading image files:
- `POST /api/v1/describe/openai` - File upload only
- `POST /api/v1/describe/ollama` - File upload only
- `POST /api/v1/describe/claude` - File upload only
- `POST /api/v1/describe/auto` - File upload only

**In Swagger UI:**
1. Click on the endpoint
2. Click "Try it out"
3. Click "Choose File" and select your image
4. Fill in other parameters (api_key, model, prompt, etc.)
5. Click "Execute"

### For Base64 Images (JSON)

Use this endpoint for base64 encoded images:
- `POST /api/v1/describe/openai/json` - JSON request with base64

**In Swagger UI:**
1. Click on the JSON endpoint
2. Click "Try it out"
3. Edit the JSON body with your base64 image
4. Click "Execute"

## Common Issues and Solutions

### Issue: "Input should be a valid dictionary" error
**Solution:** This was happening because Swagger was trying to send both form data and JSON in the same request. Now fixed by separating the endpoints.

### Issue: Need to send base64 image
**Solution:** Use the `/json` endpoint variant which accepts a JSON body.

### Issue: File upload not working
**Solution:** Make sure you're using the regular endpoint (not `/json`) and selecting a file using the "Choose File" button.

## Example Curl Commands

### File Upload
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/describe/openai' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your-image.jpg;type=image/jpeg' \
  -F 'api_key=your-api-key' \
  -F 'model=gpt-4o-mini' \
  -F 'prompt=Describe this image' \
  -F 'max_tokens=300'
```

### Base64 JSON
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/describe/openai/json' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "image_base64": "your-base64-string",
    "api_key": "your-api-key",
    "model": "gpt-4o-mini",
    "prompt": "Describe this image",
    "max_tokens": 300
  }'
```

## Best Practices

1. **Use environment variables** for API keys to avoid entering them repeatedly
2. **Choose the right endpoint**: File upload vs JSON based on your needs
3. **Check the response examples** in the documentation to understand the expected output
4. **Use meaningful prompts** to get better descriptions from the AI models
