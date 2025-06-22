# FastAPI Parameters Summary

## ✅ All Parameters Included

Our FastAPI plan now includes **ALL** parameters from the current library implementation:

### Image Description Endpoints

1. **OpenAI** (`/api/v1/describe/openai`)
   - ✅ file upload / image_base64
   - ✅ model (optional, default: "gpt-4o-mini")
   - ✅ api_key (optional)
   - ✅ prompt (optional)
   - ✅ max_tokens (optional, default: 300)

2. **Ollama** (`/api/v1/describe/ollama`)
   - ✅ file upload / image_base64
   - ✅ model (optional, default: "llama3.2-vision")
   - ✅ prompt (optional)

3. **Claude** (`/api/v1/describe/claude`)
   - ✅ file upload / image_base64
   - ✅ api_key (optional)
   - ✅ prompt (optional)
   - ✅ model (optional, default: "claude-3-opus-20240229") *[Added]*
   - ✅ max_tokens (optional, default: 1024) *[Added]*

4. **Auto-select** (`/api/v1/describe/auto`)
   - ✅ file upload / image_base64
   - ✅ model (optional)
   - ✅ prompt (optional) *[Added]*

### Document Extraction Endpoints

5. **Extract** (`/api/v1/extract/process`)
   - ✅ file upload
   - ✅ file_type ("pdf", "docx", "pptx", "html")
   - ✅ extractor_type (optional, default: "page_as_image")
   - ✅ model (optional)
   - ✅ api_key (optional)
   - ✅ prompt (optional)

### Key Improvements in FastAPI Design

1. **File Handling**: Accept both file uploads and base64 encoded images
2. **Consistent Parameters**: All image description endpoints have prompt support
3. **Configurable Defaults**: All hardcoded values are now configurable
4. **Additional Features**: Batch processing, health checks, configuration management

### Example with All Parameters

```bash
# OpenAI with all parameters
curl -X POST "http://localhost:8000/api/v1/describe/openai" \
  -F "file=@image.jpg" \
  -F "model=gpt-4-vision-preview" \
  -F "api_key=sk-..." \
  -F "prompt=Describe this image focusing on technical details" \
  -F "max_tokens=1000"

# Claude with all parameters
curl -X POST "http://localhost:8000/api/v1/describe/claude" \
  -F "file=@image.jpg" \
  -F "model=claude-3-opus-20240229" \
  -F "api_key=sk-ant-..." \
  -F "prompt=Analyze this image for accessibility issues" \
  -F "max_tokens=2000"
```
