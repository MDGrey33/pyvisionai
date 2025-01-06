# CLI and Library Instructions

## Setup

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

3. **Configure Environment Variables**
   ```bash
   # Required for image description (using GPT-4 Vision by default)
   export OPENAI_API_KEY='your-api-key'
   ```

4. **Create Required Directories**
   ```bash
   mkdir -p content/source content/extracted content/log
   ```

## Command Line Tools

After installing the package, you'll have access to two CLI commands:

### 1. Image Description CLI (`describe-image`)

The `describe-image` command allows you to describe images using different vision models.

```bash
# Basic Usage
describe-image -i path/to/image.jpg [options]

# Options:
-i, --image      Path to the image file (required)
-u, --use-case   Model to use for description:
                 - gpt4: OpenAI GPT-4 Vision (default)
                 - gpt3: OpenAI GPT-3 Vision
                 - llama: Local Llama model (requires Ollama setup)
-k, --api-key    OpenAI API key (required for gpt3/gpt4)
-v, --verbose    Print additional information

# Examples:
# Using default GPT-4 Vision
describe-image -i content/test/source/test.jpeg -v

# Using GPT-3 Vision
describe-image -i content/test/source/test.jpeg -u gpt3 -v

# Using local Llama model (requires Ollama setup)
describe-image -i content/test/source/test.jpeg -u llama -v
```

### 2. File Extraction CLI (`file-extract`)

The `file-extract` command extracts content from various file types (PDF, DOCX, PPTX).

```bash
# Basic Usage
file-extract -t file_type [options]

# Options:
-t, --type       Type of file to process (required):
                 - pdf
                 - docx
                 - pptx
-s, --source     Source file or directory (default: ./content/source)
-o, --output     Output directory (default: ./content/extracted)
-e, --extractor  Extraction method:
                 - page_as_image: Convert each page to image (default, recommended)
                 - text_and_images: Extract text and images separately

# Examples:
# Process a single PDF file (using default page-as-image method)
file-extract -t pdf -s path/to/file.pdf -o output_dir

# Process all DOCX files in a directory with specific extractor
file-extract -t docx -s input_dir -o output_dir -e text_and_images

# Process PPTX with default settings
file-extract -t pptx -s path/to/file.pptx
```

## Library Usage

### Image Description

```python
from file_extractor import describe_image_openai, describe_image_ollama

# Using GPT-4 Vision (default, recommended)
description = describe_image_openai(
    image_path="path/to/image.jpg",
    model="gpt-4o",  # default
    api_key="your-api-key",  # optional if set in environment
    max_tokens=300  # default
)

# Using local Llama model (requires Ollama setup)
description = describe_image_ollama(
    image_path="path/to/image.jpg",
    model="llama3.2-vision"  # default
)
```

### File Extraction

```python
from file_extractor import create_extractor

# Create an extractor (using default page-as-image method)
pdf_extractor = create_extractor("pdf")  # page_as_image is default

# Or specify a different extraction method
pdf_extractor = create_extractor(
    file_type="pdf",
    extractor_type="text_and_images"
)

# Process a file
output_path = pdf_extractor.extract(
    input_file="path/to/file.pdf",
    output_dir="path/to/output"
)
```

## Environment Variables

The library uses the following environment variables:

```bash
# OpenAI API Key (required for default GPT-4 Vision)
export OPENAI_API_KEY='your-api-key'

# Ollama Host (optional, only if using Llama model)
export OLLAMA_HOST='http://localhost:11434'
```

## Output Format

All extractors generate:
1. A markdown file containing:
   - Document title
   - Page content (text or image descriptions)
   - Page/slide numbers

2. Directory structure:
```
content/
├── extracted/
│   └── document_name/
│       └── document_name.md
├── source/
│   └── (your source files)
└── log/
    └── file_extractor_YYYYMMDD_HHMMSS.log
``` 