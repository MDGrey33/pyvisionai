"""Tests for benchmark logging functionality."""

import os
import json


def test_benchmark_log_structure():
    """Verify that benchmark logs are being created with correct structure."""
    log_dir = "content/log"
    log_file = os.path.join(log_dir, "benchmark.log")

    assert os.path.exists(log_file), "Benchmark log file should be created"

    with open(log_file, "r") as f:
        last_line = f.readlines()[-1]
        entry = json.loads(last_line)

        # Verify log structure
        assert "timestamp" in entry
        assert "test" in entry
        assert "metrics" in entry

        # Verify metrics structure
        metrics = entry["metrics"]
        if metrics["interface"] == "api":
            assert "setup_time" in metrics
            assert "extraction_time" in metrics
        assert "total_time" in metrics
        assert "output_size" in metrics

