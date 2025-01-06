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

## Recommended Settings

### Image Description Models
- **GPT-4 Vision** (Default): Best quality descriptions, recommended for production use
- **GPT-3.5 Vision**: Good balance of quality and speed
- **Llama (Local)**: Fast, no API costs, good for development/testing

### Extraction Methods
- **Page as Image** (Default): Best for complex layouts, consistent results
- **Text and Images**: Better for simple layouts, preserves original text

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
   pip install file-extractor

   # Using poetry
   poetry add file-extractor
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
from file_extractor import create_extractor, describe_image_openai, describe_image_ollama

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

## Parameters

### File Extraction CLI Parameters
| Parameter | Short | Description | Default | Required |
|-----------|-------|-------------|----------|----------|
| `--type`, `-t` | `-t` | File type to process (pdf, docx, pptx) | - | Yes |
| `--source`, `-s` | `-s` | Source file or directory path | `./content/source` | No |
| `--output`, `-o` | `-o` | Output directory path | `./content/extracted` | No |
| `--extractor`, `-e` | `-e` | Extraction method (text_and_images, page_as_image) | `page_as_image` | No |

### Image Description CLI Parameters
| Parameter | Short | Description | Default | Required |
|-----------|-------|-------------|----------|----------|
| `--image`, `-i` | `-i` | Path to the image file | - | Yes |
| `--model`, `-u` | `-u` | Model to use (gpt4, llama) | `gpt4` | No |
| `--api-key`, `-k` | `-k` | OpenAI API key | From env | No* |
| `--verbose`, `-v` | `-v` | Print verbose output | `False` | No |

*Required when using GPT-4 and not set in environment

### Library Function Parameters

#### `create_extractor(file_type, extractor_type="page_as_image")`
| Parameter | Type | Description | Default |
|-----------|------|-------------|----------|
| `file_type` | str | Type of file to process (pdf, docx, pptx) | - |
| `extractor_type` | str | Extraction method (text_and_images, page_as_image) | `page_as_image` |

#### `describe_image_ollama(image_path, model="llama3.2-vision")`
| Parameter | Type | Description | Default |
|-----------|------|-------------|----------|
| `image_path` | str | Path to the image file | - |
| `model` | str | Ollama model to use | `llama3.2-vision` |

#### `describe_image_openai(image_path, model="gpt-4o-mini", api_key=None, max_tokens=300)`
| Parameter | Type | Description | Default |
|-----------|------|-------------|----------|
| `image_path` | str | Path to the image file | - |
| `model` | str | OpenAI model to use | `gpt-4o-mini` |
| `api_key` | str | OpenAI API key | From env |
| `max_tokens` | int | Maximum tokens in response | 300 |

## Extraction Methods

### PDF Files
1. **Page as Image** (default):
   - Converts each page to a high-resolution image
   - Best for complex layouts or when text extraction is unreliable
   - Provides consistent results across different PDF types

2. **Text and Images**:
   - Extracts text and embedded images separately
   - Preserves original text content and formatting
   - Best for PDFs with simple layouts

### DOCX Files
1. **Page as Image** (default):
   - Converts each page to an image
   - Captures exact visual appearance
   - Best for documents with complex formatting

2. **Text and Images**:
   - Extracts text and embedded images separately
   - Preserves original text formatting
   - Best for simple documents

### PPTX Files
1. **Page as Image** (default):
   - Converts each slide to an image
   - Captures exact visual appearance
   - Best for presentations with animations or complex layouts

2. **Text and Images**:
   - Extracts text and embedded images separately
   - Preserves original text formatting
   - Best for simple presentations

## Output Format

All extractors generate:
1. A markdown file containing:
   - Document title
   - Page/slide content (text or image descriptions)
   - Page/slide numbers
2. Clean directory structure:
   ```
   output_dir/
   └── document_name.md
   ```

## Logging

The application maintains detailed logs of all operations:
- Logs are stored in `content/log/` with timestamp-based filenames
- Each run creates a new log file: `file_extractor_YYYYMMDD_HHMMSS.log`
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
