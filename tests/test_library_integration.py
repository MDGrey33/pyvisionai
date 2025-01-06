"""
Library integration tests.
"""

import os
import pytest
from pyvisionai import (
    create_extractor,
    describe_image_ollama,
    describe_image_openai
)


@pytest.fixture
def test_dirs():
    """Create and return test directories."""
    source_dir = "./content/test/source"
    output_dir = "./content/test/output"
    os.makedirs(output_dir, exist_ok=True)
    return source_dir, output_dir


def test_pdf_extraction(test_dirs):
    """Test PDF extraction using page-as-image method."""
    source_dir, output_dir = test_dirs
    pdf_path = os.path.join(source_dir, "test.pdf")
    
    # Create PDF extractor with default method (page-as-image)
    extractor = create_extractor("pdf")
    output_path = extractor.extract(pdf_path, output_dir)
    
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "# test" in content
        assert "Page 1" in content
        assert "Description:" in content


def test_docx_extraction(test_dirs):
    """Test DOCX extraction."""
    source_dir, output_dir = test_dirs
    docx_path = os.path.join(source_dir, "test.docx")
    
    # Create DOCX extractor
    extractor = create_extractor("docx")
    output_path = extractor.extract(docx_path, output_dir)
    
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "# test" in content
        assert "Description:" in content


def test_pptx_extraction(test_dirs):
    """Test PPTX extraction."""
    source_dir, output_dir = test_dirs
    pptx_path = os.path.join(source_dir, "test.pptx")
    
    # Create PPTX extractor
    extractor = create_extractor("pptx")
    output_path = extractor.extract(pptx_path, output_dir)
    
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "# test" in content
        assert "Slide 1" in content
        assert "Description:" in content


def test_image_description_gpt4(test_dirs):
    """Test image description using GPT-4."""
    source_dir, _ = test_dirs
    image_path = os.path.join(source_dir, "test.jpeg")
    
    # Use GPT-4 Vision
    description = describe_image_openai(image_path, model="gpt-4o-mini")
    assert description and len(description) > 0


def test_image_description_gpt3(test_dirs):
    """Test image description using GPT-3."""
    source_dir, _ = test_dirs
    image_path = os.path.join(source_dir, "test.jpeg")
    
    # Use GPT-3.5 Vision
    description = describe_image_openai(image_path, model="gpt-4o-mini")
    assert description and len(description) > 0


def test_image_description_llama(test_dirs):
    """Test image description using Llama."""
    source_dir, _ = test_dirs
    image_path = os.path.join(source_dir, "test.jpeg")
    
    # Use Llama model
    description = describe_image_ollama(image_path)
    assert description and len(description) > 0


def test_pdf_text_extraction(test_dirs):
    """Test PDF extraction using text-and-images method."""
    source_dir, output_dir = test_dirs
    pdf_path = os.path.join(source_dir, "test.pdf")
    
    # Create PDF extractor with text-and-images method
    extractor = create_extractor("pdf", extractor_type="text_and_images")
    output_path = extractor.extract(pdf_path, output_dir)
    
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "# test" in content
        assert "Page 1" in content
        assert "Description:" in content


def test_docx_text_extraction(test_dirs):
    """Test DOCX extraction using text-and-images method."""
    source_dir, output_dir = test_dirs
    docx_path = os.path.join(source_dir, "test.docx")
    
    # Create DOCX extractor with text-and-images method
    extractor = create_extractor("docx", extractor_type="text_and_images")
    output_path = extractor.extract(docx_path, output_dir)
    
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "# test" in content
        assert "Description:" in content 