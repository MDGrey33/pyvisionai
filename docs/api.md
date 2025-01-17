# PyVisionAI API Documentation

## Overview

PyVisionAI is a Python library for extracting and describing content from documents using Vision Language Models (LLMs). It supports multiple file formats and provides both cloud-based and local image description capabilities.

## Installation

```bash
pip install pyvisionai
```

## Core Components

### Content Extraction

The library provides extractors for various file formats:
- PDF documents
- Microsoft Word (DOCX) files
- PowerPoint (PPTX) presentations
- HTML pages

Each extractor supports two methods:
- `page_as_image`: Converts each page to an image and describes it using Vision LLM
- `text_and_images`: Extracts text and images separately (not available for HTML)

### Image Description

Two Vision LLM options are available:
- OpenAI's GPT-4 Vision (cloud-based, recommended)
- Llama Vision model (local, via Ollama)

## API Reference

### Factory Function

```python
from pyvisionai import create_extractor

def create_extractor(
    file_type: str,
    extractor_type: str = "page_as_image",
    model: str = "gpt4",
    api_key: Optional[str] = None,
    prompt: Optional[str] = None
) -> BaseExtractor:
    """
    Create an extractor instance for the specified file type.

    Args:
        file_type: Type of file to process ("pdf", "docx", "pptx", "html")
        extractor_type: Extraction method ("page_as_image" or "text_and_images")
        model: Vision model to use ("gpt4" or "llama")
        api_key: OpenAI API key (required for GPT-4 Vision)
        prompt: Custom prompt for image description

    Returns:
        An instance of the appropriate extractor class

    Raises:
        ValueError: If file_type or extractor_type is invalid
    """
```

### Base Extractor

All extractors inherit from `BaseExtractor` and implement its interface:

```python
class BaseExtractor:
    def extract(self, input_file: str, output_dir: str) -> str:
        """
        Extract content from a file.

        Args:
            input_file: Path to the input file
            output_dir: Directory to save extracted content

        Returns:
            str: Path to the generated markdown file

        Raises:
            FileNotFoundError: If input_file doesn't exist
            ExtractionError: If extraction fails
        """
```

### Image Description Functions

```python
from pyvisionai import describe_image_openai, describe_image_ollama

def describe_image_openai(
    image_path: str,
    model: str = "gpt-4-vision-preview",
    api_key: Optional[str] = None,
    prompt: Optional[str] = None,
    max_tokens: int = 300
) -> str:
    """
    Describe an image using OpenAI's Vision model.

    Args:
        image_path: Path to the image file
        model: OpenAI model name
        api_key: OpenAI API key
        prompt: Custom prompt for image description
        max_tokens: Maximum tokens in response

    Returns:
        str: Description of the image

    Raises:
        FileNotFoundError: If image file doesn't exist
        APIError: If API call fails
    """

def describe_image_ollama(
    image_path: str,
    model: str = "llama3.2-vision",
    prompt: Optional[str] = None
) -> str:
    """
    Describe an image using local Llama model via Ollama.

    Args:
        image_path: Path to the image file
        model: Ollama model name
        prompt: Custom prompt for image description

    Returns:
        str: Description of the image

    Raises:
        FileNotFoundError: If image file doesn't exist
        ConnectionError: If Ollama server is not running
    """
```

## Usage Examples

### Basic Usage

```python
from pyvisionai import create_extractor

# Extract from PDF using default settings (page_as_image + GPT-4 Vision)
extractor = create_extractor("pdf")
output_path = extractor.extract("document.pdf", "output/")

# Extract from DOCX using text_and_images method
extractor = create_extractor("docx", extractor_type="text_and_images")
output_path = extractor.extract("document.docx", "output/")

# Extract from HTML using local Llama model
extractor = create_extractor("html", model="llama")
output_path = extractor.extract("page.html", "output/")
```

### Custom Image Description

```python
from pyvisionai import describe_image_openai

# Describe image with custom prompt
description = describe_image_openai(
    "image.jpg",
    prompt="List all the objects visible in this image",
    max_tokens=500
)

# Use local Llama model
from pyvisionai import describe_image_ollama
description = describe_image_ollama(
    "image.jpg",
    prompt="Describe the main subject of this image"
)
```

## Error Handling

```python
from pyvisionai import create_extractor
from pyvisionai.exceptions import ExtractionError

try:
    extractor = create_extractor("pdf")
    output = extractor.extract("document.pdf", "output/")
except FileNotFoundError:
    print("Input file not found")
except ExtractionError as e:
    print(f"Extraction failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required for GPT-4 Vision)
- `OLLAMA_HOST`: Ollama server host (default: "http://localhost:11434")

### Default Settings

- Default extraction method: `page_as_image`
- Default vision model: `gpt4`
- Default image description prompt: "Extract the exact text as present in the image and write one sentence about each visual in the image"

## Performance Considerations

1. **Memory Usage**
   - Large PDF files may require significant memory when using `page_as_image` method
   - Consider using `text_and_images` method for large documents

2. **Processing Speed**
   - Cloud-based GPT-4 Vision is generally faster than local Llama model
   - HTML processing requires browser rendering and may be slower

3. **Batch Processing**
   - Process multiple files in parallel for better performance
   - Monitor memory usage when processing large batches

## Best Practices

1. **File Types**
   - Use `text_and_images` for text-heavy documents
   - Use `page_as_image` for documents with complex layouts
   - Always use `page_as_image` for HTML (only supported method)

2. **Image Description**
   - Use specific prompts for better results
   - Consider token limits when using GPT-4 Vision
   - Ensure Ollama server is running when using local model

3. **Error Handling**
   - Always implement proper error handling
   - Check input file existence before processing
   - Validate output directory permissions
