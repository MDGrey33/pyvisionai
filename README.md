# Content Extractor with Vision LLM

Extract and describe content from documents using Vision Language Models.

## Requirements

- Python 3.8 or higher
- Operating system: Windows, macOS, or Linux
- Disk space: At least 1GB free space (more if using local Llama model)

## Features

- Extract text and images from PDF, DOCX, and PPTX files
- Describe images using local (Ollama) or cloud-based (OpenAI) Vision Language Models
- Save extracted text and image descriptions in markdown format
- Support for both CLI and library usage
- Multiple extraction methods for different use cases
- Detailed logging with timestamps for all operations

## Installation

1. **Install System Dependencies**
   ```bash
   # macOS (using Homebrew)
   brew install --cask libreoffice  # Required for DOCX/PPTX processing
   brew install poppler             # Required for PDF processing

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install libreoffice poppler-utils

   # Windows
   # Download and install:
   # - LibreOffice: https://www.libreoffice.org/download/download/
   # - Poppler: http://blog.alivate.com.au/poppler-windows/
   # Add poppler's bin directory to your system PATH
   ```

2. **Install the Package**
   ```bash
   # Using pip
   pip install pyvisionai

   # Using poetry
   poetry add pyvisionai
   ```

3. **Create Working Directories** (optional)
   ```bash
   # The package will create these automatically if they don't exist
   mkdir -p content/source content/extracted content/log
   ```

4. **Setup for Image Description**

   For cloud image description (default, recommended):
   ```bash
   # Set OpenAI API key
   export OPENAI_API_KEY='your-api-key'
   ```

   For local image description (optional):
   ```bash
   # Start Ollama server
   ollama serve

   # Pull the required model
   ollama pull llama3.2-vision
   ```

## Usage

### Command Line Interface

1. **Extract Content from Files**
   ```bash
   # Process a single file (using default page-as-image method)
   file-extract -t pdf -s path/to/file.pdf -o output_dir
   file-extract -t docx -s path/to/file.docx -o output_dir
   file-extract -t pptx -s path/to/file.pptx -o output_dir

   # Process with specific extractor
   file-extract -t pdf -s input.pdf -o output_dir -e text_and_images

   # Process all files in a directory
   file-extract -t pdf -s input_dir -o output_dir
   ```

2. **Describe Images**
   ```bash
   # Using GPT-4 Vision (default, recommended)
   describe-image -i path/to/image.jpg

   # Using local Llama model
   describe-image -i path/to/image.jpg -u llama

   # Additional options
   describe-image -i image.jpg -v  # Verbose output
   ```

### Library Usage

```python
from pyvisionai import create_extractor, describe_image_openai, describe_image_ollama

# 1. Extract content from files
extractor = create_extractor("pdf")  # or "docx" or "pptx"
output_path = extractor.extract("input.pdf", "output_dir")

# With specific extraction method
extractor = create_extractor("pdf", extractor_type="text_and_images")
output_path = extractor.extract("input.pdf", "output_dir")

# 2. Describe images
# Using GPT-4 Vision (default, recommended)
description = describe_image_openai(
    "image.jpg",
    model="gpt-4o-mini",  # default
    api_key="your-api-key",  # optional if set in environment
    max_tokens=300  # default
)

# Using local Llama model
description = describe_image_ollama(
    "image.jpg",
    model="llama3.2-vision"  # default
)
```

## Logging

The application maintains detailed logs of all operations:
- Logs are stored in `content/log/` with timestamp-based filenames
- Each run creates a new log file: `pyvisionai_YYYYMMDD_HHMMSS.log`
- Logs include:
  - Timestamp for each operation
  - Processing steps and their status
  - Error messages and warnings
  - Extraction method used
  - Input and output file paths

## Environment Variables

```bash
# Required for OpenAI Vision (if using cloud description)
export OPENAI_API_KEY='your-api-key'

# Optional: Ollama host (if using local description)
export OLLAMA_HOST='http://localhost:11434'
```

## License

This project is licensed under the [Apache License 2.0](LICENSE).
