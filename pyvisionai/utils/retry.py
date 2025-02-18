"""Retry mechanism for handling transient failures."""

import logging
import time
from enum import Enum
from typing import Callable, Optional, TypeVar

import requests

T = TypeVar('T')


class RetryStrategy(Enum):
    """Available retry delay strategies."""

    EXPONENTIAL = "exponential"  # Exponential backoff
    LINEAR = "linear"  # Linear backoff
    CONSTANT = "constant"  # Constant delay


class RetryableError(Exception):
    """Base class for errors that should trigger retry."""

    pass


class APIError(RetryableError):
    """Base class for API-related errors."""

    pass


class RateLimitError(APIError):
    """Error raised when API rate limit is exceeded."""

    pass


class TemporaryError(APIError):
    """Error raised for temporary API issues (5xx errors)."""

    pass


class ConnectionError(APIError):
    """Error raised for network connectivity issues."""

    pass


def is_retryable_http_error(e: Exception) -> bool:
    """
    Check if an HTTP error should trigger a retry.

    Args:
        e: The exception to check

    Returns:
        bool: True if the error should trigger a retry
    """
    # Handle Anthropic errors
    if e.__class__.__name__ == "APIError":
        error_msg = str(e).lower()
        return (
            "rate limit" in error_msg
            or "server error" in error_msg
            or "overloaded" in error_msg
            or "529" in error_msg
        )

    # Handle OpenAI errors
    if e.__class__.__name__ == "OpenAIError":
        error_msg = str(e).lower()
        return "rate limit" in error_msg or "server error" in error_msg

    if isinstance(e, requests.exceptions.RequestException):
        if isinstance(e, requests.exceptions.HTTPError):
            # Retry on rate limits (429), server errors (5xx), and overloaded (529)
            return e.response.status_code in [429, 529] + list(
                range(500, 600)
            )
        # Retry on connection errors, timeouts etc.
        return isinstance(
            e,
            (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ),
        )
    return False


def convert_error(e: Exception) -> Exception:
    """Convert API errors to appropriate retry errors."""
    error_msg = str(e).lower()
    if "rate limit" in error_msg:
        return ConnectionError("Rate limit exceeded")
    elif "server error" in error_msg:
        return ConnectionError("Internal server error")
    elif "overloaded" in error_msg or "529" in error_msg:
        return ConnectionError("Service overloaded")
    return e


class RetryManager:
    """Manages retry logic for operations that may fail transiently."""

    def __init__(
        self,
        max_attempts: int = 3,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the retry manager.

        Args:
            max_attempts: Maximum number of attempts (including first try)
            strategy: Retry delay strategy to use
            base_delay: Base delay between retries in seconds
            max_delay: Maximum delay between retries in seconds
            logger: Logger instance to use (creates new if None)
        """
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if base_delay <= 0:
            raise ValueError("base_delay must be > 0")
        if max_delay < base_delay:
            raise ValueError("max_delay must be >= base_delay")

        self.max_attempts = max_attempts
        self.strategy = strategy
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.logger = logger or logging.getLogger(__name__)

    def execute(self, operation: Callable[[], T]) -> T:
        """
        Execute an operation with retry logic.

        Args:
            operation: Callable that may raise RetryableError

        Returns:
            The result of the operation if successful

        Raises:
            RetryableError: If max retries exceeded
            Exception: Any non-retryable error from operation
        """
        last_error = None

        for attempt in range(self.max_attempts):
            try:
                return operation()
            except Exception as e:
                # Convert HTTP errors to retryable errors
                if isinstance(e, requests.exceptions.ConnectionError):
                    error = ConnectionError(str(e))
                elif is_retryable_http_error(e):
                    error = convert_error(e)
                elif not isinstance(e, RetryableError):
                    raise
                else:
                    error = e

                last_error = error
                if attempt + 1 < self.max_attempts:
                    delay = self._calculate_delay(attempt)
                    self.logger.warning(
                        f"Attempt {attempt + 1} failed: {str(error)}. "
                        f"Retrying in {delay:.1f}s"
                    )
                    time.sleep(delay)
                continue

        # Re-raise the last error
        raise last_error

    def _calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for next retry based on strategy.

        Args:
            attempt: Current attempt number (0-based)

        Returns:
            float: Delay in seconds
        """
        if self.strategy == RetryStrategy.EXPONENTIAL:
            delay = self.base_delay * (2**attempt)
        elif self.strategy == RetryStrategy.LINEAR:
            delay = self.base_delay * (attempt + 1)
        else:  # CONSTANT
            delay = self.base_delay

        return min(delay, self.max_delay)
