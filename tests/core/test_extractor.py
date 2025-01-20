"""Tests for the BaseExtractor class."""

import pytest

from pyvisionai.core.extractor import BaseExtractor


def test_cannot_instantiate_base_extractor():
    """Test that BaseExtractor cannot be instantiated directly."""
    with pytest.raises(
        TypeError, match=r"Can't instantiate abstract class"
    ):
        BaseExtractor()


def test_must_implement_extract():
    """Test that concrete classes must implement the extract method."""

    class IncompleteExtractor(BaseExtractor):
        pass

    with pytest.raises(
        TypeError, match=r"Can't instantiate abstract class"
    ):
        IncompleteExtractor()


def test_concrete_implementation():
    """Test that a concrete implementation with extract method can be instantiated."""

    class ConcreteExtractor(BaseExtractor):
        def extract(self, file_path: str, output_dir: str) -> str:
            return "test.md"

    extractor = ConcreteExtractor()
    assert isinstance(extractor, BaseExtractor)
    result = extractor.extract("test.pdf", "output/")
    assert isinstance(result, str)
    assert result == "test.md"


def test_extract_method_interface():
    """Test that the extract method follows the expected interface."""

    class TestExtractor(BaseExtractor):
        def extract(self, file_path: str, output_dir: str) -> str:
            assert isinstance(
                file_path, str
            ), "file_path must be a string"
            assert isinstance(
                output_dir, str
            ), "output_dir must be a string"
            return "test.md"

    extractor = TestExtractor()
    result = extractor.extract("test.pdf", "output/")
    assert isinstance(result, str)


def test_extract_method_documentation():
    """Test that the extract method has proper documentation."""
    assert BaseExtractor.extract.__doc__ is not None
    assert "file_path" in BaseExtractor.extract.__doc__
    assert "output_dir" in BaseExtractor.extract.__doc__
    assert "Returns" in BaseExtractor.extract.__doc__
