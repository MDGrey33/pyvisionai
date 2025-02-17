"""Tests for benchmark logging functionality."""

import json
from datetime import datetime
from pathlib import Path

import pytest

from pyvisionai.utils.benchmark import (
    BenchmarkEntry,
    BenchmarkLogger,
    BenchmarkMetrics,
)
from tests.conftest import log_benchmark


@pytest.fixture
def sample_benchmark_data(benchmark_log_file):
    """Generate sample benchmark data for testing."""
    log_dir = benchmark_log_file.parent

    # Generate CLI benchmark
    log_benchmark(
        "pdf",
        "page_as_image",
        {
            "interface": "cli",
            "cli_time": 13.5,
            "output_size": 2500,
        },
        log_dir=log_dir,
    )

    # Generate API benchmark
    log_benchmark(
        "docx",
        "text_and_images",
        {
            "interface": "api",
            "setup_time": 0.1,
            "extraction_time": 5.2,
            "output_size": 1800,
        },
        log_dir=log_dir,
    )


def test_benchmark_log_structure(
    sample_benchmark_data, benchmark_log_file
):
    """Verify that benchmark logs are being created with correct structure."""
    assert (
        benchmark_log_file.exists()
    ), "Benchmark log file should be created"

    with open(benchmark_log_file, "r") as f:
        lines = f.readlines()
        assert len(lines) >= 2, "Expected at least 2 benchmark entries"

        # Parse entries
        entries = [
            BenchmarkEntry.from_dict(json.loads(line)) for line in lines
        ]
        cli_entries = [
            e for e in entries if e.metrics.interface == "cli"
        ]
        api_entries = [
            e for e in entries if e.metrics.interface == "api"
        ]

        assert cli_entries, "Expected at least one CLI benchmark entry"
        assert api_entries, "Expected at least one API benchmark entry"

        # Test CLI benchmark entry
        cli_entry = cli_entries[-1]
        assert cli_entry.test["file_type"] == "pdf"
        assert cli_entry.test["method"] == "page_as_image"
        assert cli_entry.metrics.cli_time is not None
        assert cli_entry.metrics.output_size > 0

        # Test API benchmark entry
        api_entry = api_entries[-1]
        assert api_entry.test["file_type"] == "docx"
        assert api_entry.test["method"] == "text_and_images"
        assert api_entry.metrics.setup_time is not None
        assert api_entry.metrics.extraction_time is not None
        assert api_entry.metrics.output_size > 0


def test_benchmark_metrics_validation():
    """Test validation of benchmark metrics."""
    # Test invalid output size
    with pytest.raises(
        ValueError, match="output_size must be a non-negative integer"
    ):
        BenchmarkMetrics(
            interface="cli", output_size=-1, cli_time=1.0
        ).validate()

    # Test invalid interface
    with pytest.raises(
        ValueError, match="interface must be either 'cli' or 'api'"
    ):
        BenchmarkMetrics(
            interface="invalid", output_size=100, cli_time=1.0
        ).validate()

    # Test missing cli_time for CLI interface
    with pytest.raises(
        ValueError, match="cli_time is required for CLI interface"
    ):
        BenchmarkMetrics(interface="cli", output_size=100).validate()

    # Test missing extraction_time for API interface
    with pytest.raises(
        ValueError,
        match="extraction_time is required for API interface",
    ):
        BenchmarkMetrics(interface="api", output_size=100).validate()


def test_benchmark_normalization(benchmark_log_file):
    """Test normalization of benchmark metrics."""
    log_dir = benchmark_log_file.parent

    # Test CLI metrics with total_time
    log_benchmark(
        "pdf",
        "page_as_image",
        {
            "interface": "cli",
            "total_time": 10.0,
            "output_size": 1000,
        },
        log_dir=log_dir,
    )

    # Test API metrics without setup_time
    log_benchmark(
        "docx",
        "text_and_images",
        {
            "interface": "api",
            "extraction_time": 5.0,
            "output_size": 1000,
        },
        log_dir=log_dir,
    )

    with open(benchmark_log_file, "r") as f:
        lines = f.readlines()
        entries = [
            BenchmarkEntry.from_dict(json.loads(line)) for line in lines
        ]

        # Check CLI metrics normalization
        cli_entry = entries[0]
        assert cli_entry.metrics.cli_time == 10.0

        # Check API metrics normalization
        api_entry = entries[1]
        assert api_entry.metrics.setup_time == 0
        assert api_entry.metrics.cli_time == 5.0


def test_concurrent_logging(benchmark_log_file):
    """Test concurrent logging with file locking."""
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    log_dir = benchmark_log_file.parent
    start_event = Event()
    logs_written = []

    def log_concurrently():
        start_event.wait()
        try:
            log_benchmark(
                "test",
                "concurrent",
                {
                    "interface": "cli",
                    "cli_time": 1.0,
                    "output_size": 100,
                },
                log_dir=log_dir,
            )
            logs_written.append(True)
        except Exception:
            logs_written.append(False)

    # Start multiple threads
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(log_concurrently) for _ in range(5)]
        start_event.set()  # Start all threads simultaneously

    # Verify all logs were written successfully
    assert all(logs_written)

    # Verify log file integrity
    with open(benchmark_log_file, "r") as f:
        lines = f.readlines()
        assert len(lines) == 5
        # Verify each line is valid JSON
        for line in lines:
            entry = BenchmarkEntry.from_dict(json.loads(line))
            assert entry.metrics.cli_time == 1.0
            assert entry.metrics.output_size == 100
