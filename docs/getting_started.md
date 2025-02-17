# Getting Started with PyVisionAI

This guide will help you get started with PyVisionAI, a powerful tool for extracting and describing content from documents using Vision Language Models.

## Prerequisites

Before using PyVisionAI, ensure you have:

1. Python 3.11 or higher installed
2. System dependencies installed:
   ```bash
   # macOS
   brew install --cask libreoffice  # For DOCX/PPTX
   brew install poppler             # For PDF

   # Ubuntu/Debian
   sudo apt-get install -y libreoffice poppler-utils

   # Windows
   # Install LibreOffice and Poppler manually
   ```

## Installation

1. **Install via pip**
   ```bash
   pip install pyvisionai
   ```

2. Set up environment variables:
   ```bash
   # For OpenAI Vision (recommended)
   export OPENAI_API_KEY='your-api-key'

## Configuration

### API Keys

1. **Cloud-based Models (Recommended)**

   Choose one or both of the following:

   ```bash
   # For GPT-4 Vision
   export OPENAI_API_KEY='your-openai-key'

   # For Claude Vision
   export ANTHROPIC_API_KEY='your-anthropic-key'
   ```

2. **Local Model (Optional)**
   ```bash
   # First install and start Ollama
   brew install ollama    # macOS
   # Or for Linux
   curl -fsSL https://ollama.com/install.sh | sh
   # Or for Windows, download from:
   # https://ollama.com/download/windows

   ollama serve
   ollama pull llama3.2-vision
   ```

## Basic Usage

### Command Line Interface

1. **Extract Content from Documents**
   ```bash
   # Basic usage (uses GPT-4 Vision by default)
   file-extract -t pdf -s document.pdf -o output_dir

   # Using Claude Vision
   file-extract -t pdf -s document.pdf -o output_dir -m claude

   # Using local Llama model
   file-extract -t pdf -s document.pdf -o output_dir -m llama
   ```

2. **Describe Images**
   ```bash
   # Using GPT-4 Vision (default)
   describe-image -i image.jpg

   # Using Claude Vision
   describe-image -i image.jpg -u claude -k your-anthropic-key

   # Using local Llama model
   describe-image -i image.jpg -u llama

   # With custom prompt
   describe-image -i image.jpg -p "Describe the main colors and objects"
   ```

### Python Library

```python
from pyvisionai import (
    create_extractor,
    describe_image_openai,
    describe_image_claude,
    describe_image_ollama
)

# 1. Extract content from documents
# Using GPT-4 Vision (default)
extractor = create_extractor("pdf")
output_path = extractor.extract("document.pdf", "output_dir")

# Using Claude Vision
extractor = create_extractor("pdf", model="claude")
output_path = extractor.extract("document.pdf", "output_dir")

# Using local Llama model
extractor = create_extractor("pdf", model="llama")
output_path = extractor.extract("document.pdf", "output_dir")

# 2. Describe images
# Using GPT-4 Vision
description = describe_image_openai(
    "image.jpg",
    api_key="your-openai-key",  # optional if set in environment
    prompt="Describe the main objects"  # optional
)

# Using Claude Vision
description = describe_image_claude(
    "image.jpg",
    api_key="your-anthropic-key",  # optional if set in environment
    prompt="List the colors present"  # optional
)

# Using local Llama model
description = describe_image_ollama(
    "image.jpg",
    prompt="Describe the scene"  # optional
)
```

## Supported File Types

- PDF (`.pdf`)
- Word Documents (`.docx`)
- PowerPoint Presentations (`.pptx`)
- HTML Pages (`.html`, `.htm`)

## Vision Models

1. **GPT-4 Vision (Default)**
   - Cloud-based model by OpenAI
   - Requires API key
   - Best for general-purpose image description
   - Supports detailed custom prompts

2. **Claude Vision**
   - Cloud-based model by Anthropic
   - Requires API key
   - Excellent for detailed analysis
   - Strong at identifying text in images

3. **Llama Vision**
   - Local model via Ollama
   - No API key required
   - Good for basic image description
   - Runs entirely on your machine

## Extraction Methods

1. **page_as_image (Default)**
   - Converts each page to an image
   - Sends to vision model for description
   - Best for maintaining layout
   - Works with all file types

2. **text_and_images**
   - Extracts text and images separately
   - More efficient for text-heavy documents
   - Better for searchable output
   - Not available for HTML files

## Output Format

The extracted content is saved in markdown format:

```markdown
# Document Title

## Page 1
[Description of page content]

### Extracted Text
[Text content if available]

### Images
1. [Description of image 1]
2. [Description of image 2]

## Page 2
...
```

## Advanced Usage

### Custom Prompts

```bash
# CLI
describe-image -i image.jpg -p "List all visible text in the image"

# Python
description = describe_image_claude(
    "image.jpg",
    prompt="Identify and transcribe any visible text"
)
```

### Batch Processing

```bash
# Process all PDFs in a directory
file-extract -t pdf -s input_dir -o output_dir

# Process with specific model
file-extract -t pdf -s input_dir -o output_dir -m claude
```

### Error Handling

```python
try:
    description = describe_image_claude("image.jpg")
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Error processing image: {e}")
```

## Next Steps

1. Read the [API Documentation](api.md) for detailed reference
2. Check out the [Examples](../examples/) directory
3. Learn about [Testing](testing.md) your implementations
4. Review [Contributing Guidelines](../CONTRIBUTING.md)

## Common Issues

1. **Missing Dependencies**
   ```bash
   # If you see LibreOffice errors:
   brew install --cask libreoffice  # macOS

   # If you see Poppler errors:
   brew install poppler  # macOS
   ```

2. **Memory Issues with Large Files**
   - Use `text_and_images` method instead of `page_as_image`
   - Process files in smaller batches
   - Increase system swap space if needed

3. **Slow Processing**
   - Consider using cloud-based GPT-4 Vision for faster results
   - Process files in parallel for batch operations
   - Use SSD storage for better I/O performance
