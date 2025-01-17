"""Tests for custom prompts example."""

import os
import shutil
import tempfile
from unittest.mock import Mock, patch

import pytest

from examples.custom_prompts import (
    SPECIALIZED_PROMPTS,
    example_technical_documentation,
    example_business_report,
    example_research_paper,
    example_chart_analysis,
    example_table_extraction,
    example_combined_analysis,
    example_custom_prompt_builder,
)

# Reuse test data paths from test_examples.py
TEST_DATA_DIR = os.path.join("tests", "data")
TEST_PDF = os.path.join(TEST_DATA_DIR, "technical_doc.pdf")
TEST_PPTX = os.path.join(TEST_DATA_DIR, "charts.pptx")
TEST_DOCX = os.path.join(TEST_DATA_DIR, "report.docx")
TEST_CHART = os.path.join(TEST_DATA_DIR, "chart.png")

@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir)

@pytest.fixture
def setup_test_files(temp_output_dir):
    """Set up test files and directories."""
    os.makedirs(TEST_DATA_DIR, exist_ok=True)
    
    # Create test files if they don't exist
    test_files = {
        TEST_PDF: "Technical documentation content",
        TEST_PPTX: "Business presentation content",
        TEST_DOCX: "Report with tables",
        TEST_CHART: "Chart image content"
    }
    
    for filepath, content in test_files.items():
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write(content)
    
    yield

def test_specialized_prompts():
    """Test that all specialized prompts are properly defined."""
    expected_prompts = ["technical", "business", "academic", "chart", "table"]
    assert all(prompt in SPECIALIZED_PROMPTS for prompt in expected_prompts)
    assert all(isinstance(SPECIALIZED_PROMPTS[p], str) for p in SPECIALIZED_PROMPTS)

@patch("examples.custom_prompts.create_extractor")
def test_technical_documentation(mock_create_extractor, temp_output_dir, setup_test_files):
    """Test technical documentation extraction."""
    # Setup mock
    mock_extractor = Mock()
    mock_extractor.extract.return_value = "output.md"
    mock_create_extractor.return_value = mock_extractor
    
    # Run example
    with patch("examples.custom_prompts.print"):
        example_technical_documentation()
    
    # Verify
    mock_create_extractor.assert_called_once_with(
        "pdf",
        prompt=SPECIALIZED_PROMPTS["technical"]
    )
    mock_extractor.extract.assert_called_once()
    args = mock_extractor.extract.call_args[0]
    assert args[0].endswith("technical_doc.pdf")
    assert args[1].endswith("technical")

@patch("examples.custom_prompts.create_extractor")
def test_business_report(mock_create_extractor, temp_output_dir, setup_test_files):
    """Test business report extraction."""
    # Setup mock
    mock_extractor = Mock()
    mock_extractor.extract.return_value = "output.md"
    mock_create_extractor.return_value = mock_extractor
    
    # Run example
    with patch("examples.custom_prompts.print"):
        example_business_report()
    
    # Verify
    mock_create_extractor.assert_called_once_with(
        "pptx",
        prompt=SPECIALIZED_PROMPTS["business"]
    )
    mock_extractor.extract.assert_called_once()
    args = mock_extractor.extract.call_args[0]
    assert args[0].endswith("charts.pptx")
    assert args[1].endswith("business")

@patch("examples.custom_prompts.describe_image_openai")
def test_chart_analysis(mock_describe_image, temp_output_dir, setup_test_files):
    """Test chart analysis."""
    # Setup mock
    mock_describe_image.return_value = "Chart description"
    
    # Run example
    with patch("examples.custom_prompts.print"):
        example_chart_analysis()
    
    # Verify
    mock_describe_image.assert_called_once_with(
        os.path.join("example_data", "chart.png"),
        prompt=SPECIALIZED_PROMPTS["chart"]
    )

@patch("examples.custom_prompts.create_extractor")
def test_combined_analysis(mock_create_extractor, temp_output_dir, setup_test_files):
    """Test combined prompt analysis."""
    # Setup mock
    mock_extractor = Mock()
    mock_extractor.extract.return_value = "output.md"
    mock_create_extractor.return_value = mock_extractor
    
    # Run example
    with patch("examples.custom_prompts.print"):
        example_combined_analysis()
    
    # Verify
    mock_create_extractor.assert_called_once()
    call_args = mock_create_extractor.call_args[1]
    # Check that combined prompt includes all components
    assert "technical" in call_args["prompt"]
    assert "chart" in call_args["prompt"]
    assert "table" in call_args["prompt"]
    mock_extractor.extract.assert_called_once()

def test_custom_prompt_builder():
    """Test custom prompt builder functionality."""
    # Run example with mock
    with patch("examples.custom_prompts.create_extractor") as mock_create:
        with patch("examples.custom_prompts.print"):
            example_custom_prompt_builder()
        
        # Verify prompt construction
        call_args = mock_create.call_args[1]
        prompt = call_args["prompt"]
        
        # Check prompt components
        assert "Extract and describe all text content" in prompt
        assert SPECIALIZED_PROMPTS["chart"] in prompt
        assert SPECIALIZED_PROMPTS["table"] in prompt

@patch("examples.custom_prompts.create_extractor")
def test_error_handling(mock_create_extractor, temp_output_dir, setup_test_files):
    """Test error handling in examples."""
    # Setup mock to raise exception
    mock_extractor = Mock()
    mock_extractor.extract.side_effect = Exception("Processing failed")
    mock_create_extractor.return_value = mock_extractor
    
    # Test error handling in each example
    with patch("examples.custom_prompts.print") as mock_print:
        example_technical_documentation()
        mock_print.assert_any_call(
            "Error processing technical doc: Exception: Processing failed"
        )
        
        example_business_report()
        mock_print.assert_any_call(
            "Error processing business report: Exception: Processing failed"
        )

def test_prompt_combinations():
    """Test different combinations of custom prompts."""
    def build_prompt(has_charts: bool = False, 
                    has_tables: bool = False, 
                    has_code: bool = False) -> str:
        """Local version of prompt builder for testing."""
        prompt_parts = ["Extract and describe all text content."]
        
        if has_charts:
            prompt_parts.append(SPECIALIZED_PROMPTS["chart"])
        if has_tables:
            prompt_parts.append(SPECIALIZED_PROMPTS["table"])
        if has_code:
            prompt_parts.append(
                "Extract all code blocks, maintaining proper formatting."
            )
        
        return " ".join(prompt_parts)
    
    # Test different combinations
    basic_prompt = build_prompt()
    assert "Extract and describe all text content" in basic_prompt
    assert SPECIALIZED_PROMPTS["chart"] not in basic_prompt
    
    chart_prompt = build_prompt(has_charts=True)
    assert SPECIALIZED_PROMPTS["chart"] in chart_prompt
    assert SPECIALIZED_PROMPTS["table"] not in chart_prompt
    
    full_prompt = build_prompt(has_charts=True, has_tables=True, has_code=True)
    assert SPECIALIZED_PROMPTS["chart"] in full_prompt
    assert SPECIALIZED_PROMPTS["table"] in full_prompt
    assert "code blocks" in full_prompt 