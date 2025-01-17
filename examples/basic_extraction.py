#!/usr/bin/env python3
"""
Basic extraction examples using PyVisionAI.

This script demonstrates the most common use cases for extracting content
from different types of files using PyVisionAI.
"""

import os
from pyvisionai import create_extractor, describe_image_openai

def ensure_dir(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def example_pdf_extraction():
    """Example: Extract content from a PDF file."""
    print("\n=== PDF Extraction Example ===")
    
    # Create PDF extractor with default settings (page_as_image + GPT-4 Vision)
    extractor = create_extractor("pdf")
    
    try:
        # Extract content from PDF
        output_path = extractor.extract(
            "example_data/sample.pdf",
            "output/pdf"
        )
        print(f"PDF content extracted to: {output_path}")
    except FileNotFoundError:
        print("Error: PDF file not found")
    except Exception as e:
        print(f"Error extracting PDF: {e}")

def example_docx_extraction():
    """Example: Extract content from a Word document."""
    print("\n=== Word Document Extraction Example ===")
    
    # Create DOCX extractor using text_and_images method
    extractor = create_extractor(
        "docx",
        extractor_type="text_and_images"
    )
    
    try:
        # Extract content from DOCX
        output_path = extractor.extract(
            "example_data/sample.docx",
            "output/docx"
        )
        print(f"DOCX content extracted to: {output_path}")
    except FileNotFoundError:
        print("Error: DOCX file not found")
    except Exception as e:
        print(f"Error extracting DOCX: {e}")

def example_pptx_extraction():
    """Example: Extract content from a PowerPoint presentation."""
    print("\n=== PowerPoint Extraction Example ===")
    
    # Create PPTX extractor with custom prompt
    extractor = create_extractor(
        "pptx",
        prompt="List all text content and describe any diagrams or charts"
    )
    
    try:
        # Extract content from PPTX
        output_path = extractor.extract(
            "example_data/sample.pptx",
            "output/pptx"
        )
        print(f"PPTX content extracted to: {output_path}")
    except FileNotFoundError:
        print("Error: PPTX file not found")
    except Exception as e:
        print(f"Error extracting PPTX: {e}")

def example_html_extraction():
    """Example: Extract content from a web page."""
    print("\n=== Web Page Extraction Example ===")
    
    # Create HTML extractor
    extractor = create_extractor("html")
    
    try:
        # Extract content from HTML
        output_path = extractor.extract(
            "https://example.com",
            "output/html"
        )
        print(f"HTML content extracted to: {output_path}")
    except Exception as e:
        print(f"Error extracting HTML: {e}")

def example_image_description():
    """Example: Describe individual images."""
    print("\n=== Image Description Example ===")
    
    try:
        # Describe image using OpenAI Vision
        description = describe_image_openai(
            "example_data/sample_image.jpg",
            prompt="Describe the main elements and any text in this image"
        )
        print("Image Description:")
        print(description)
    except FileNotFoundError:
        print("Error: Image file not found")
    except Exception as e:
        print(f"Error describing image: {e}")

def main():
    """Run all examples."""
    # Create output directories
    ensure_dir("output/pdf")
    ensure_dir("output/docx")
    ensure_dir("output/pptx")
    ensure_dir("output/html")
    
    # Run examples
    example_pdf_extraction()
    example_docx_extraction()
    example_pptx_extraction()
    example_html_extraction()
    example_image_description()
    
    print("\nAll examples completed!")

if __name__ == "__main__":
    main() 