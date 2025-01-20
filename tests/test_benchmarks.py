"""Tests for benchmark logging functionality."""

import json
import os
from datetime import datetime

import pytest

from tests.conftest import log_benchmark


@pytest.fixture
def sample_benchmark_data(setup_test_env):
    """Generate sample benchmark data for testing."""
    # Generate CLI benchmark
    log_benchmark(
        "pdf",
        "page_as_image",
        {
            "interface": "cli",
            "total_time": 13.5,
            "output_size": 2500,
        },
    )

    # Generate API benchmark
    log_benchmark(
        "docx",
        "text_and_images",
        {
            "interface": "api",
            "setup_time": 0.1,
            "extraction_time": 5.2,
            "total_time": 5.3,
            "output_size": 1800,
        },
    )


def test_benchmark_log_structure(sample_benchmark_data):
    """Verify that benchmark logs are being created with correct structure."""
    log_dir = "content/log"
    log_file = os.path.join(log_dir, "benchmark.log")

    assert os.path.exists(
        log_file
    ), "Benchmark log file should be created"

    with open(log_file, "r") as f:
        lines = f.readlines()
        assert len(lines) >= 2, "Expected at least 2 benchmark entries"

        # Test CLI benchmark entry
        cli_entry = json.loads(lines[-2])
        assert cli_entry["test"]["file_type"] == "pdf"
        assert cli_entry["test"]["method"] == "page_as_image"
        assert cli_entry["metrics"]["interface"] == "cli"
        assert "total_time" in cli_entry["metrics"]
        assert "output_size" in cli_entry["metrics"]

        # Test API benchmark entry
        api_entry = json.loads(lines[-1])
        assert api_entry["test"]["file_type"] == "docx"
        assert api_entry["test"]["method"] == "text_and_images"
        assert api_entry["metrics"]["interface"] == "api"
        assert "setup_time" in api_entry["metrics"]
        assert "extraction_time" in api_entry["metrics"]
        assert "total_time" in api_entry["metrics"]
        assert "output_size" in api_entry["metrics"]
