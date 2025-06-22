# API Parameters Comparison

## Current Library Parameters vs FastAPI Plan

### 1. Image Description APIs

| Function | Current Library Parameters | FastAPI Plan | Missing in Plan? |
|----------|---------------------------|--------------|------------------|
| **describe_image_openai** | - image_path<br>- model (optional)<br>- api_key (optional)<br>- max_tokens=300<br>- prompt (optional) | ✅ All included | None |
| **describe_image_ollama** | - image_path<br>- model (optional)<br>- prompt (optional) | ✅ All included | None |
| **describe_image_claude** | - image_path<br>- api_key (optional)<br>- prompt (optional) | ✅ All included | ⚠️ Missing: model parameter<br>⚠️ Missing: max_tokens |
| **describe_image** (auto) | - image_path<br>- model (optional) | ✅ Included | ⚠️ Missing: prompt parameter |

### 2. Document Extraction APIs

| Function | Current Library Parameters | FastAPI Plan | Missing in Plan? |
|----------|---------------------------|--------------|------------------|
| **create_extractor** | - file_type<br>- extractor_type="page_as_image"<br>- model=DEFAULT_IMAGE_MODEL<br>- api_key (optional)<br>- prompt (optional) | ✅ All included | None |
| **BaseExtractor.extract** | - input_file<br>- output_dir | ✅ All included | None |

### 3. Additional Parameters Found in Implementation

#### Claude Model Specifics:
- Uses hardcoded model: `"claude-3-opus-20240229"`
- Uses hardcoded max_tokens: `1024`
- Should expose these as configurable parameters

#### OpenAI Model Specifics:
- Default model: `"gpt-4o-mini"`
- Configurable max_tokens with default `300`

#### Ollama Model Specifics:
- Default model: `"llama3.2-vision"`
- No max_tokens parameter (uses model default)

### 4. Recommended Updates to FastAPI Plan

1. **Add to Claude endpoint:**
   ```python
   model: str = "claude-3-opus-20240229"  # Make configurable
   max_tokens: int = 1024  # Make configurable
   ```

2. **Add to auto-select endpoint:**
   ```python
   prompt: Optional[str] = None  # Add prompt support
   ```

3. **Consider adding to all endpoints:**
   ```python
   timeout: Optional[int] = 30  # API timeout in seconds
   retry_attempts: Optional[int] = 3  # Number of retries
   ```

### 5. File Upload Considerations

For FastAPI, we need to handle both:
- **File uploads** (multipart/form-data) - recommended
- **Base64 encoded images** (JSON) - for programmatic access

Example enhanced request model:
```python
class ImageDescriptionRequest(BaseModel):
    # Option 1: Base64 encoded image
    image_base64: Optional[str] = None

    # Option 2: Reference to uploaded file
    file_id: Optional[str] = None

    # Common parameters
    model: Optional[str] = None
    api_key: Optional[str] = None
    prompt: Optional[str] = None
    max_tokens: Optional[int] = None

    # Advanced parameters
    timeout: Optional[int] = 30
    retry_attempts: Optional[int] = 3
```
