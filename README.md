# PyVisionAI
# Content Extractor and Image Description with Vision LLM

Extract and describe content from documents using Vision Language Models.

## Repository

https://github.com/MDGrey33/pyvisionai

## Requirements

- Python 3.8 or higher
- Operating system: Windows, macOS, or Linux
- Disk space: At least 1GB free space (more if using local Llama model)

## Features

- Extract text and images from PDF, DOCX, PPTX, and HTML files
- Capture interactive HTML pages as images with full rendering
- Describe images using local (Ollama) or cloud-based (OpenAI) Vision Language Models
- Save extracted text and image descriptions in markdown format
- Support for both CLI and library usage
- Multiple extraction methods for different use cases
- Detailed logging with timestamps for all operations
- Customizable image description prompts

## Installation

1. **Install System Dependencies**
   ```bash
   # macOS (using Homebrew)
   brew install --cask libreoffice  # Required for DOCX/PPTX processing
   brew install poppler             # Required for PDF processing
   pip install playwright          # Required for HTML processing
   playwright install              # Install browser dependencies

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y libreoffice  # Required for DOCX/PPTX processing
   sudo apt-get install -y poppler-utils # Required for PDF processing
   pip install playwright               # Required for HTML processing
   playwright install                   # Install browser dependencies

   # Windows
   # Download and install:
   # - LibreOffice: https://www.libreoffice.org/download/download/
   # - Poppler: http://blog.alivate.com.au/poppler-windows/
   # Add poppler's bin directory to your system PATH
   pip install playwright
   playwright install
   ```

2. **Install PyVisionAI**
   ```bash
   # Using pip
   pip install pyvisionai

   # Using poetry (will automatically install playwright as a dependency)
   poetry add pyvisionai
   poetry run playwright install  # Install browser dependencies
   ```

## Directory Structure

By default, PyVisionAI uses the following directory structure:
```
content/
├── source/      # Default input directory for files to process
├── extracted/   # Default output directory for processed files
└── log/         # Directory for log files and benchmarks
```

These directories are created automatically when needed, but you can:
1. Create them manually:
   ```bash
   mkdir -p content/source content/extracted content/log
   ```
2. Override them with custom paths:
   ```bash
   # Specify custom input and output directories
   file-extract -t pdf -s /path/to/inputs -o /path/to/outputs

   # Process a single file with custom output
   file-extract -t pdf -s ~/documents/file.pdf -o ~/results
   ```

Note: While the default directories provide a organized structure, you're free to use any directory layout that suits your needs by specifying custom paths with the `-s` (source) and `-o` (output) options.

## Setup for Image Description

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

## Features

- Extract text and images from PDF, DOCX, PPTX, and HTML files
- Capture interactive HTML pages as images with full rendering
- Describe images using local (Ollama) or cloud-based (OpenAI) Vision Language Models
- Save extracted text and image descriptions in markdown format
- Support for both CLI and library usage
- Multiple extraction methods for different use cases
- Detailed logging with timestamps for all operations

## Usage

### Command Line Interface

1. **Extract Content from Files**
   ```bash
   # Process a single file (using default page-as-image method)
   file-extract -t pdf -s path/to/file.pdf -o output_dir
   file-extract -t docx -s path/to/file.docx -o output_dir
   file-extract -t pptx -s path/to/file.pptx -o output_dir
   file-extract -t html -s path/to/file.html -o output_dir

   # Process with specific extractor
   file-extract -t pdf -s input.pdf -o output_dir -e text_and_images

   # Process all files in a directory
   file-extract -t pdf -s input_dir -o output_dir

   # Example with custom prompt
   file-extract -t pdf -s document.pdf -o output_dir -p "Extract the exact text as present in the image and write one sentence about each visual in the image"
   ```

   **Note:** The custom prompt for file extraction will affect the content of the output document. In case of page_as_image It should contain instructions to extract text and describe visuals. Variations are acceptable as long as they encompass these tasks. Avoid prompts like "What's the color of this picture?" as they may not yield the desired results.

2. **Describe Images**
   ```bash
   # Using GPT-4 Vision (default, recommended)
   describe-image -i path/to/image.jpg

   # Using local Llama model
   describe-image -i path/to/image.jpg -u llama

   # Using custom prompt
   describe-image -i image.jpg -p "List the main colors in this image"

   # Additional options
   describe-image -i image.jpg -v  # Verbose output
   ```

### Library Usage

```python
from pyvisionai import create_extractor, describe_image_openai, describe_image_ollama

# 1. Extract content from files
extractor = create_extractor("pdf")  # or "docx", "pptx", or "html"
output_path = extractor.extract("input.pdf", "output_dir")

# With specific extraction method
extractor = create_extractor("pdf", extractor_type="text_and_images")
output_path = extractor.extract("input.pdf", "output_dir")

# Extract from HTML (always uses page_as_image method)
extractor = create_extractor("html")
output_path = extractor.extract("page.html", "output_dir")

# 2. Describe images
# Using GPT-4 Vision (default, recommended)
description = describe_image_openai(
    "image.jpg",
    model="gpt-4o-mini",  # default
    api_key="your-api-key",  # optional if set in environment
    max_tokens=300,  # default
    prompt="Describe this image focusing on colors and textures"  # optional custom prompt
)

# Using local Llama model
description = describe_image_ollama(
    "image.jpg",
    model="llama3.2-vision",  # default
    prompt="List the main objects in this image"  # optional custom prompt
)
```

## Logging

The application maintains detailed logs of all operations:
- By default, logs are stored in `content/log/` with timestamp-based filenames
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

## Command Parameters

### `file-extract` Command
```bash
file-extract [-h] -t TYPE -s SOURCE -o OUTPUT [-e EXTRACTOR] [-m MODEL] [-k API_KEY] [-v]

Required Arguments:
  -t, --type TYPE         File type to process (pdf, docx, pptx, html)
  -s, --source SOURCE     Source file or directory path
  -o, --output OUTPUT     Output directory path

Optional Arguments:
  -h, --help             Show help message and exit
  -e, --extractor TYPE   Extraction method:
                         - page_as_image: Convert pages to images (default)
                         - text_and_images: Extract text and images separately
                         Note: HTML only supports page_as_image
  -m, --model MODEL      Vision model for image description:
                         - gpt4: GPT-4 Vision (default, recommended)
                         - llama: Local Llama model
  -k, --api-key KEY      OpenAI API key (can also be set via OPENAI_API_KEY env var)
  -v, --verbose          Enable verbose logging
  -p, --prompt TEXT      Custom prompt for image description
```

### `describe-image` Command
```bash
describe-image [-h] -i IMAGE [-m MODEL] [-k API_KEY] [-t MAX_TOKENS] [-v] [-p PROMPT]

Required Arguments:
  -i, --image IMAGE      Path to image file

Optional Arguments:
  -h, --help            Show help message and exit
  -m, --model MODEL     Vision model to use:
                        - gpt4: GPT-4 Vision (default, recommended)
                        - llama: Local Llama model
  -k, --api-key KEY     OpenAI API key (can also be set via OPENAI_API_KEY env var)
  -t, --max-tokens NUM  Maximum tokens for response (default: 300)
  -p, --prompt TEXT     Custom prompt for image description
  -v, --verbose         Enable verbose logging
```

## Examples

### File Extraction Examples
```bash
# Basic usage with defaults (page_as_image method, GPT-4 Vision)
file-extract -t pdf -s document.pdf -o output_dir
file-extract -t html -s webpage.html -o output_dir  # HTML always uses page_as_image

# Specify extraction method (not applicable for HTML)
file-extract -t docx -s document.docx -o output_dir -e text_and_images

# Use local Llama model for image description
file-extract -t pptx -s slides.pptx -o output_dir -m llama

# Process all PDFs in a directory with verbose logging
file-extract -t pdf -s input_dir -o output_dir -v

# Use custom OpenAI API key
file-extract -t pdf -s document.pdf -o output_dir -k "your-api-key"

# Use custom prompt for image descriptions
file-extract -t pdf -s document.pdf -o output_dir -p "Focus on text content and layout"
```

### Image Description Examples
```bash
# Basic usage with defaults (GPT-4 Vision)
describe-image -i photo.jpg

# Use local Llama model
describe-image -i photo.jpg -m llama

# Use custom prompt
describe-image -i photo.jpg -p "List the main colors and their proportions"

# Customize token limit
describe-image -i photo.jpg -t 500

# Enable verbose logging
describe-image -i photo.jpg -v

# Use custom OpenAI API key
describe-image -i photo.jpg -k "your-api-key"

# Combine options
describe-image -i photo.jpg -m llama -p "Describe the lighting and shadows" -v
```

## Custom Prompts

PyVisionAI supports custom prompts for both file extraction and image description. Custom prompts allow you to control how content is extracted and described.

### Using Custom Prompts

1. **CLI Usage**
   ```bash
   # File extraction with custom prompt
   file-extract -t pdf -s document.pdf -o output_dir -p "Extract all text verbatim and describe any diagrams or images in detail"

   # Image description with custom prompt
   describe-image -i image.jpg -p "List the main colors and describe the layout of elements"
   ```

2. **Library Usage**
   ```python
   # File extraction with custom prompt
   extractor = create_extractor(
       "pdf",
       extractor_type="page_as_image",
       prompt="Extract all text exactly as it appears and provide detailed descriptions of any charts or diagrams"
   )
   output_path = extractor.extract("input.pdf", "output_dir")

   # Image description with custom prompt
   description = describe_image_openai(
       "image.jpg",
       prompt="Focus on spatial relationships between objects and any text content"
   )
   ```

3. **Environment Variable**
   ```bash
   # Set default prompt via environment variable
   export FILE_EXTRACTOR_PROMPT="Extract text and describe visual elements with emphasis on layout"
   ```

### Writing Effective Prompts

1. **For Page-as-Image Method**
   - Include instructions for both text extraction and visual description since the entire page is processed as an image
   - Example: "Extract the exact text as it appears on the page and describe any images, diagrams, or visual elements in detail"

2. **For Text-and-Images Method**
   - Focus only on image description since text is extracted separately
   - The model only sees the images, not the text content
   - Example: "Describe the visual content, focusing on what the image represents and any visual elements it contains"

3. **For Image Description**
   - Be specific about what aspects to focus on
   - Example: "Describe the main elements, their arrangement, and any text visible in the image"

Note: For page-as-image method, prompts must include both text extraction and visual description instructions as the entire page is processed as an image. For text-and-images method, prompts should focus solely on image description as text is handled separately.

## Contributing

We welcome contributions to PyVisionAI! Whether you're fixing bugs, improving documentation, or proposing new features, your help is appreciated.

Please read our [Contributing Guidelines](CONTRIBUTING.md) for detailed information on:
- Setting up your development environment
- Code style and standards
- Testing requirements
- Pull request process
- Documentation guidelines

### Quick Start for Contributors

1. Fork and clone the repository
2. Install development dependencies:
   ```bash
   pip install poetry
   poetry install
   ```
3. Install pre-commit hooks:
   ```bash
   poetry run pre-commit install
   ```
4. Make your changes
5. Run tests:
   ```bash
   poetry run pytest
   ```
6. Submit a pull request

For more detailed instructions, see [CONTRIBUTING.md](CONTRIBUTING.md).
