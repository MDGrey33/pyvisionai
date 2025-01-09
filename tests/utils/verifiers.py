"""Content verification utilities for tests."""


def verify_basic_content(content: str):
    """Verify basic content requirements."""
    assert len(content) > 0, "Content should not be empty"
    assert (
        "Description:" in content
    ), "Content should include image descriptions"
    assert "# test" in content, "Content should include document title"


def verify_pdf_content(content: str):
    """Verify PDF-specific content."""
    assert (
        "Page 1" in content
    ), "PDF content should include page numbers"
    assert (
        "Exploring Nature" in content
    ), "Expected document title not found in PDF"
    assert (
        "[Image" in content and "forest" in content.lower()
    ), "Expected forest description not found in PDF"


def verify_pptx_content(content: str):
    """Verify PPTX-specific content."""
    assert (
        "Slide 1" in content
    ), "PPTX content should include slide numbers"
    if "[Image" in content:
        assert any(
            term in content.lower() for term in ["tablet", "person"]
        ), "Expected image content not found in PPTX"


def verify_docx_content(content: str):
    """Verify DOCX-specific content."""
    assert (
        "Exploring Nature" in content
    ), "Expected document title not found in DOCX"
    if "[Image" in content:
        assert (
            "forest" in content.lower()
        ), "Expected forest description not found in DOCX"


def verify_html_content(content: str):
    """Verify HTML-specific content."""
    assert (
        "Page 1" in content
    ), "HTML content should include page numbers"
    assert (
        "Exploring Nature" in content
    ), "Expected document title not found in HTML"
    assert (
        "interactive" in content.lower()
    ), "Expected interactive elements description not found in HTML"
    assert (
        "biodiversity" in content.lower()
    ), "Expected biodiversity section not found in HTML"
    assert (
        "[Image" in content and "forest" in content.lower()
    ), "Expected forest description not found in HTML"


# Content verification mapping
content_verifiers = {
    "pdf": verify_pdf_content,
    "docx": verify_docx_content,
    "pptx": verify_pptx_content,
    "html": verify_html_content,
}
