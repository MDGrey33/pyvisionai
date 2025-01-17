"""Performance metrics utilities for tests."""


def print_performance_metrics(
    file_type: str,
    method: str,
    setup_time: float,
    extraction_time: float,
    output_size: int,
    interface: str = "API",
):
    """Print performance metrics in a consistent format."""
    total_time = setup_time + extraction_time
    print(f"\n{file_type.upper()} ({method}) {interface} Performance:")
    if interface == "API":
        print(f"Setup time: {setup_time:.2f}s")
        print(f"Extraction time: {extraction_time:.2f}s")
    print(f"Total time: {total_time:.2f}s")
    print(f"Output size: {output_size / 1024:.2f}KB")
