# PyVisionAI FastAPI Specification

This document outlines all the APIs in the PyVisionAI library and their parameters for creating a FastAPI interface.

## 1. Image Description APIs

### 1.1 describe_image_openai
**Endpoint:** `POST /api/v1/describe/openai`

**Description:** Describe an image using OpenAI's GPT-4 Vision model.

**Parameters:**
- `image_path` (str): Path to the image file
- `model` (str, optional): Name of the OpenAI model to use (default: "gpt-4o-mini")
- `api_key` (str, optional): OpenAI API key (optional if set in environment)
- `max_tokens` (int, optional): Maximum tokens in the response (default: 300)
- `prompt` (str, optional): Custom prompt for image description (default: DEFAULT_PROMPT)

**Returns:**
- `description` (str): Description of the image

---

### 1.2 describe_image_ollama
**Endpoint:** `POST /api/v1/describe/ollama`

**Description:** Describe an image using Ollama's Llama3.2 Vision model.

**Parameters:**
- `image_path` (str): Path to the image file
- `model` (str, optional): Name of the Ollama model to use (default: "llama3.2-vision")
- `prompt` (str, optional): Custom prompt for image description (default: DEFAULT_PROMPT)

**Returns:**
- `description` (str): Description of the image

---

### 1.3 describe_image_claude
**Endpoint:** `POST /api/v1/describe/claude`

**Description:** Describe an image using Claude Vision.

**Parameters:**
- `image_path` (str): Path to the image file
- `api_key` (str, optional): Anthropic API key (optional if set in environment)
- `prompt` (str, optional): Custom prompt for image description (default: DEFAULT_PROMPT)
- `model` (str, optional): Claude model to use (default: "claude-3-opus-20240229")
- `max_tokens` (int, optional): Maximum tokens in response (default: 1024)

**Returns:**
- `description` (str): Image description

---

### 1.4 describe_image (Auto-select model)
**Endpoint:** `POST /api/v1/describe/auto`

**Description:** Describe an image using the default or specified model with automatic fallback.

**Parameters:**
- `image_path` (str): Path to the image file
- `model` (str, optional): Optional model name to use (default: uses configured default)
- `prompt` (str, optional): Custom prompt for image description (default: DEFAULT_PROMPT)

**Returns:**
- `description` (str): Description of the image
- `model_used` (str): The model that was actually used

---

## 2. Document Extraction APIs

### 2.1 create_extractor
**Endpoint:** `POST /api/v1/extract/create`

**Description:** Create an extractor instance for document processing.

**Parameters:**
- `file_type` (str): Type of file to process ("pdf", "docx", "pptx", "html")
- `extractor_type` (str, optional): Type of extraction (default: "page_as_image")
  - "page_as_image": Convert each page to image (recommended)
  - "text_and_images": Extract text and images separately
- `model` (str, optional): Model to use for image descriptions (default: DEFAULT_IMAGE_MODEL)
- `api_key` (str, optional): API key for the model
- `prompt` (str, optional): Custom prompt for image description

**Returns:**
- `extractor_id` (str): Unique identifier for the created extractor

---

### 2.2 extract
**Endpoint:** `POST /api/v1/extract/process`

**Description:** Extract content from a document.

**Parameters:**
- `input_file` (str): Path to the input file
- `output_dir` (str): Directory to save extracted content
- `file_type` (str): Type of file ("pdf", "docx", "pptx", "html")
- `extractor_type` (str, optional): Type of extraction (default: "page_as_image")
- `model` (str, optional): Model to use for image descriptions
- `api_key` (str, optional): API key for the model
- `prompt` (str, optional): Custom prompt for image description

**Returns:**
- `output_path` (str): Path to the generated markdown file
- `job_id` (str): Unique job identifier for tracking

---

## 3. Batch Processing APIs

### 3.1 process_directory
**Endpoint:** `POST /api/v1/batch/process`

**Description:** Process all supported files in a directory.

**Parameters:**
- `input_dir` (str): Input directory path
- `output_dir` (str): Output directory path
- `file_types` (List[str], optional): List of file extensions to process (default: all supported)
- `max_workers` (int, optional): Maximum number of parallel workers (default: 4)
- `model` (str, optional): Model to use for image descriptions
- `api_key` (str, optional): API key for the model
- `prompt` (str, optional): Custom prompt for image description

**Returns:**
- `batch_id` (str): Unique batch identifier
- `total_files` (int): Total number of files to process
- `status` (str): Initial status ("queued")

---

### 3.2 get_batch_status
**Endpoint:** `GET /api/v1/batch/status/{batch_id}`

**Description:** Get the status of a batch processing job.

**Parameters:**
- `batch_id` (str): Batch identifier

**Returns:**
- `batch_id` (str): Batch identifier
- `status` (str): Current status ("processing", "completed", "failed")
- `total_files` (int): Total number of files
- `processed_files` (int): Number of processed files
- `successful` (int): Number of successful extractions
- `failed` (int): Number of failed extractions
- `errors` (List[str]): List of error messages

---

## 4. File Upload APIs

### 4.1 upload_image
**Endpoint:** `POST /api/v1/upload/image`

**Description:** Upload an image file for processing.

**Parameters:**
- `file` (UploadFile): Image file to upload

**Returns:**
- `file_id` (str): Unique identifier for the uploaded file
- `file_path` (str): Path where the file was saved

---

### 4.2 upload_document
**Endpoint:** `POST /api/v1/upload/document`

**Description:** Upload a document file for extraction.

**Parameters:**
- `file` (UploadFile): Document file to upload (PDF, DOCX, PPTX, HTML)

**Returns:**
- `file_id` (str): Unique identifier for the uploaded file
- `file_path` (str): Path where the file was saved
- `file_type` (str): Detected file type

---

## 5. Health & Status APIs

### 5.1 health_check
**Endpoint:** `GET /api/v1/health`

**Description:** Check the health status of the API.

**Returns:**
- `status` (str): "healthy" or "unhealthy"
- `version` (str): API version
- `models_available` (List[str]): List of available models

---

### 5.2 get_available_models
**Endpoint:** `GET /api/v1/models/available`

**Description:** Get list of available vision models and their status.

**Returns:**
- `models` (List[Dict]): List of model information
  - `name` (str): Model name
  - `type` (str): Model type ("openai", "ollama", "claude")
  - `available` (bool): Whether the model is currently available
  - `requires_api_key` (bool): Whether an API key is required

---

## 6. Configuration APIs

### 6.1 update_default_prompt
**Endpoint:** `PUT /api/v1/config/prompt`

**Description:** Update the default prompt used for image descriptions.

**Parameters:**
- `prompt` (str): New default prompt

**Returns:**
- `success` (bool): Whether the update was successful
- `prompt` (str): The updated prompt

---

### 6.2 update_default_model
**Endpoint:** `PUT /api/v1/config/model`

**Description:** Update the default model used for image descriptions.

**Parameters:**
- `model` (str): New default model name

**Returns:**
- `success` (bool): Whether the update was successful
- `model` (str): The updated model name

---

## Request/Response Models

### ImageDescriptionRequest
```python
class ImageDescriptionRequest(BaseModel):
    image_path: str
    model: Optional[str] = None
    api_key: Optional[str] = None
    prompt: Optional[str] = None
    max_tokens: Optional[int] = 300  # For OpenAI only
```

### ImageDescriptionResponse
```python
class ImageDescriptionResponse(BaseModel):
    description: str
    model_used: str
    processing_time: float
```

### ExtractionRequest
```python
class ExtractionRequest(BaseModel):
    input_file: str
    output_dir: str
    file_type: str
    extractor_type: str = "page_as_image"
    model: Optional[str] = None
    api_key: Optional[str] = None
    prompt: Optional[str] = None
```

### ExtractionResponse
```python
class ExtractionResponse(BaseModel):
    job_id: str
    output_path: str
    status: str
    processing_time: float
```

### BatchProcessRequest
```python
class BatchProcessRequest(BaseModel):
    input_dir: str
    output_dir: str
    file_types: Optional[List[str]] = None
    max_workers: int = 4
    model: Optional[str] = None
    api_key: Optional[str] = None
    prompt: Optional[str] = None
```

### BatchProcessResponse
```python
class BatchProcessResponse(BaseModel):
    batch_id: str
    total_files: int
    status: str
    estimated_time: Optional[float] = None
```

## Error Responses

All endpoints should return appropriate HTTP status codes and error messages:

```python
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int
```

Common error codes:
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (missing or invalid API key)
- 404: Not Found (file or resource not found)
- 422: Unprocessable Entity (validation error)
- 500: Internal Server Error
- 503: Service Unavailable (model not available)

## Authentication

For production deployment, consider implementing:
- API key authentication for the FastAPI endpoints
- Rate limiting per API key
- Usage tracking and quotas

## WebSocket Support

Consider adding WebSocket endpoints for:
- Real-time batch processing progress updates
- Streaming extraction results for large documents
