"""Benchmark management utilities."""

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union

from filelock import FileLock

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkMetrics:
    """Container for benchmark metrics."""

    interface: str
    output_size: int
    cli_time: Optional[float] = None
    setup_time: Optional[float] = None
    extraction_time: Optional[float] = None

    def validate(self) -> None:
        """Validate metric values."""
        if (
            not isinstance(self.output_size, int)
            or self.output_size < 0
        ):
            raise ValueError(
                "output_size must be a non-negative integer"
            )

        if self.interface not in ["cli", "api"]:
            raise ValueError("interface must be either 'cli' or 'api'")

        if self.interface == "cli" and self.cli_time is None:
            raise ValueError("cli_time is required for CLI interface")

        if self.interface == "api" and not (
            self.cli_time or self.extraction_time
        ):
            raise ValueError(
                "Either cli_time or extraction_time is required for API interface"
            )


@dataclass
class BenchmarkEntry:
    """Container for benchmark data."""

    test: Dict[str, str]
    metrics: BenchmarkMetrics

    @classmethod
    def from_dict(cls, data: Dict) -> 'BenchmarkEntry':
        """Create BenchmarkEntry from dictionary."""
        return cls(
            test=data["test"],
            metrics=BenchmarkMetrics(**data["metrics"]),
        )


class MetricNormalizer:
    """Handles normalization of benchmark metrics."""

    @staticmethod
    def normalize(metrics: Dict) -> BenchmarkMetrics:
        """Normalize metrics to standard format.

        For CLI interface:
            - Uses cli_time as the primary timing metric
        For API interface:
            - Uses extraction_time if available, falls back to cli_time
            - setup_time is optional and defaults to 0
        """
        if metrics.get("interface") == "cli":
            return BenchmarkMetrics(
                interface="cli",
                output_size=metrics["output_size"],
                cli_time=metrics.get("cli_time")
                or metrics.get("total_time"),
            )
        else:
            # For API, use extraction_time if available, otherwise fall back to cli_time
            setup_time = metrics.get("setup_time", 0)
            total_time = metrics.get("cli_time", 0)
            extraction_time = metrics.get("extraction_time", total_time)

            return BenchmarkMetrics(
                interface="api",
                output_size=metrics["output_size"],
                setup_time=setup_time,
                extraction_time=extraction_time,
                cli_time=total_time or (setup_time + extraction_time),
            )


class BenchmarkLogger:
    """Handles benchmark logging with file locking."""

    def __init__(self, log_dir: Union[str, Path]):
        self.log_dir = Path(log_dir)
        self.log_file = self.log_dir / "benchmark.log"
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging directory."""
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log(self, file_type: str, method: str, metrics: Dict) -> None:
        """Log benchmark entry with file locking."""
        try:
            # Normalize metrics
            normalized_metrics = MetricNormalizer.normalize(metrics)
            normalized_metrics.validate()

            # Create entry
            entry = BenchmarkEntry(
                test={
                    "file_type": file_type,
                    "method": method,
                    "timestamp": datetime.now().isoformat(),
                },
                metrics=normalized_metrics,
            )

            # Write to log file with lock
            lock_file = str(self.log_file) + ".lock"
            with FileLock(lock_file):
                with open(self.log_file, "a") as f:
                    f.write(json.dumps(asdict(entry)) + "\n")

            # Log to console
            logger.info(
                f"Benchmark - {file_type} ({method}): "
                f"CLI Time: {normalized_metrics.cli_time:.2f}s, "
                f"Output Size: {normalized_metrics.output_size} bytes"
            )

        except Exception as e:
            logger.error(f"Failed to log benchmark: {str(e)}")
            raise
