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
   pip install pyvisionai

   # Using poetry
   poetry add pyvisionai
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

## Command Line Interface

### Extract Content from Files

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

### Describe Images

```bash
# Using GPT-4 Vision (default, recommended)
describe-image -i path/to/image.jpg

# Using local Llama model
describe-image -i path/to/image.jpg -u llama

# Additional options
describe-image -i image.jpg -v  # Verbose output
```

## Library Usage

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

## Output Format

All extractors generate:
1. A markdown file containing:
   - Document title
   - Page/slide content (text or image descriptions)
   - Page/slide numbers
2. Clean directory structure:
   ```
   output_dir/
   └── pyvisionai_YYYYMMDD_HHMMSS.log
   ``` 