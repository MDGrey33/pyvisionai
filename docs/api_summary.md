# PyVisionAI API Summary

## Core Library APIs

### 1. Image Description Functions

#### `describe_image_openai()`
```python
def describe_image_openai(
    image_path: str,
    model: Optional[str] = None,  # default: "gpt-4o-mini"
    api_key: Optional[str] = None,
    max_tokens: int = 300,
    prompt: Optional[str] = None  # default: DEFAULT_PROMPT
) -> str
```

#### `describe_image_ollama()`
```python
def describe_image_ollama(
    image_path: str,
    model: Optional[str] = None,  # default: "llama3.2-vision"
    prompt: Optional[str] = None  # default: DEFAULT_PROMPT
) -> str
```

#### `describe_image_claude()`
```python
def describe_image_claude(
    image_path: str,
    api_key: Optional[str] = None,
    prompt: Optional[str] = None  # default: DEFAULT_PROMPT
) -> str
```

#### `describe_image()` (Auto-select with fallback)
```python
def describe_image(
    image_path: str,
    model: Optional[str] = None  # default: DEFAULT_IMAGE_MODEL
) -> str
```

### 2. Document Extraction Functions

#### `create_extractor()`
```python
def create_extractor(
    file_type: str,  # "pdf", "docx", "pptx", "html"
    extractor_type: str = "page_as_image",  # or "text_and_images"
    model: str = DEFAULT_IMAGE_MODEL,  # "llama" or "gpt4"
    api_key: Optional[str] = None,
    prompt: Optional[str] = None
) -> BaseExtractor
```

#### `BaseExtractor.extract()`
```python
def extract(
    input_file: str,
    output_dir: str
) -> str  # Returns path to generated markdown file
```

### 3. CLI Commands

#### `describe-image`
```bash
describe-image \
  -s/--source IMAGE_PATH \
  -m/--model MODEL_NAME \
  -k/--api-key API_KEY \
  -p/--prompt CUSTOM_PROMPT \
  -v/--verbose
```

#### `file-extract`
```bash
file-extract \
  -t/--type FILE_TYPE \
  -s/--source INPUT_FILE \
  -o/--output OUTPUT_DIR \
  -e/--extractor EXTRACTOR_TYPE \
  -m/--model MODEL_NAME \
  -k/--api-key API_KEY \
  -p/--prompt CUSTOM_PROMPT \
  -v/--verbose
```

## Constants and Defaults

- `DEFAULT_IMAGE_MODEL`: "llama" (configurable)
- `DEFAULT_PROMPT`: "Describe this image in detail. Include all visible text, objects, people, and activities."
- `OPENAI_MODEL_NAME`: "gpt-4o-mini"
- `OLLAMA_MODEL_NAME`: "llama3.2-vision"

## Supported File Types

- **PDF**: Both page_as_image and text_and_images
- **DOCX**: Both page_as_image and text_and_images
- **PPTX**: Both page_as_image and text_and_images
- **HTML**: Only page_as_image

## Extractor Types

1. **page_as_image** (Recommended):
   - Converts each page/slide to an image
   - Describes the entire page using vision models
   - Better for maintaining layout and visual context

2. **text_and_images**:
   - Extracts text and images separately
   - Describes only the images
   - May lose layout information

## Example Usage

### Python Library
```python
from pyvisionai import describe_image_openai, create_extractor

# Describe an image
description = describe_image_openai("image.jpg", api_key="your-key")

# Extract from PDF
extractor = create_extractor("pdf", "page_as_image", model="gpt4")
output_path = extractor.extract("document.pdf", "output/")
```

### Batch Processing (Example Pattern)
```python
from pyvisionai import create_extractor
from concurrent.futures import ThreadPoolExecutor

class BatchProcessor:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.extractors = {
            ".pdf": create_extractor("pdf"),
            ".docx": create_extractor("docx"),
            ".pptx": create_extractor("pptx"),
            ".html": create_extractor("html"),
        }

    def process_file(self, input_path, output_dir):
        # Process individual file
        ...

    def process_directory(self, input_dir, output_dir):
        # Process all files in directory
        ...
```
