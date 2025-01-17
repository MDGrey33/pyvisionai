# Getting Started with PyVisionAI

This guide will help you get up and running with PyVisionAI quickly. We'll cover installation, basic setup, and common use cases.

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

1. Install PyVisionAI using pip:
   ```bash
   pip install pyvisionai
   ```

2. Set up environment variables:
   ```bash
   # For OpenAI Vision (recommended)
   export OPENAI_API_KEY='your-api-key'
   
   # For local Llama (optional)
   # First install and start Ollama
   brew install ollama    # macOS
   ollama serve
   ollama pull llama3.2-vision
   ```

## Quick Start

### 1. Extract Text and Images from a PDF

```python
from pyvisionai import create_extractor

# Create a PDF extractor
extractor = create_extractor("pdf")

# Extract content (will use GPT-4 Vision by default)
output_path = extractor.extract(
    "path/to/document.pdf",
    "output_directory"
)

print(f"Extracted content saved to: {output_path}")
```

### 2. Process a Word Document

```python
# Create a DOCX extractor with text_and_images method
extractor = create_extractor(
    "docx",
    extractor_type="text_and_images"
)

# Extract content
output_path = extractor.extract(
    "path/to/document.docx",
    "output_directory"
)
```

### 3. Capture and Process a Web Page

```python
# Create an HTML extractor
extractor = create_extractor("html")

# Extract content from a URL
output_path = extractor.extract(
    "https://example.com",
    "output_directory"
)
```

### 4. Describe Individual Images

```python
from pyvisionai import describe_image_openai

# Using OpenAI's Vision model
description = describe_image_openai(
    "path/to/image.jpg",
    prompt="Describe the main elements in this image"
)

print(description)
```

## Common Use Cases

### 1. Batch Processing Documents

```python
import os
from pyvisionai import create_extractor

def process_directory(input_dir: str, output_dir: str):
    # Create extractors for different file types
    extractors = {
        ".pdf": create_extractor("pdf"),
        ".docx": create_extractor("docx"),
        ".pptx": create_extractor("pptx")
    }
    
    for filename in os.listdir(input_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext in extractors:
            input_path = os.path.join(input_dir, filename)
            try:
                output_path = extractors[ext].extract(
                    input_path,
                    output_dir
                )
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Use the function
process_directory("documents", "extracted_content")
```

### 2. Custom Image Description

```python
from pyvisionai import create_extractor

# Create extractor with custom prompt
extractor = create_extractor(
    "pdf",
    prompt="List all text elements and describe any charts or diagrams"
)

# Process document
output_path = extractor.extract("report.pdf", "output")
```

### 3. Using Local Model for Privacy

```python
# Create extractor using local Llama model
extractor = create_extractor(
    "pdf",
    model="llama",
    prompt="Extract text and describe visual elements"
)

output_path = extractor.extract("confidential.pdf", "output")
```

## Output Format

PyVisionAI generates a markdown file containing:
1. Extracted text
2. Embedded images (if using text_and_images method)
3. Image descriptions
4. Source file metadata

Example output structure:
```markdown
# Document Title

## Page 1
[Extracted text content...]

### Images
![Image 1](./images/page1_image1.png)
Description: A bar chart showing sales data for Q1 2024...

## Page 2
[Extracted text content...]
...
```

## Next Steps

- Check out the [API Documentation](api.md) for detailed reference
- Learn about [Performance Optimization](performance.md)
- See [Examples](examples/) for more use cases
- Read the [Troubleshooting Guide](troubleshooting.md)

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