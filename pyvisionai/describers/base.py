"""Base image description functionality."""

import logging
import os
from abc import ABC, abstractmethod
from typing import Dict, Optional, Type

from ..utils.config import DEFAULT_IMAGE_MODEL

logger = logging.getLogger(__name__)


class VisionModel(ABC):
    """Base class for vision models."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        prompt: Optional[str] = None,
    ):
        """Initialize the model."""
        self.api_key = api_key
        self.prompt = prompt
        logger.debug(f"Initializing {self.__class__.__name__}")

    @abstractmethod
    def describe_image(self, image_path: str) -> str:
        """Describe an image using this model."""
        pass

    def validate_config(self) -> None:
        """Validate the model configuration."""
        try:
            self._validate_config()
            logger.debug("Configuration validation successful")
        except Exception as e:
            logger.error("Configuration validation failed")
            raise

    @abstractmethod
    def _validate_config(self) -> None:
        """Internal validation implementation."""
        pass


class ModelFactory:
    """Factory for creating vision models."""

    _models: Dict[str, Type[VisionModel]] = {}

    @classmethod
    def register_model(
        cls, name: str, model_class: Type[VisionModel]
    ) -> None:
        """Register a model with the factory."""
        logger.info(f"Registering model type: {name}")
        cls._models[name] = model_class

    @classmethod
    def create_model(
        cls,
        model_type: Optional[str] = None,
        api_key: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> VisionModel:
        """Create a model instance."""
        try:
            if model_type not in cls._models:
                raise ValueError(
                    f"Unsupported model type: {model_type}"
                )

            model = cls._models[model_type](
                api_key=api_key, prompt=prompt
            )
            logger.debug("Model creation successful")
            return model
        except Exception as e:
            logger.error("Model creation failed")
            raise


def describe_image(image_path: str, model: Optional[str] = None) -> str:
    """
    Describe the contents of an image using the specified model.

    Args:
        image_path: Path to the image file
        model: Optional model name to use for description (default: uses configured default)

    Returns:
        str: Description of the image
    """
    # Use configured default if no model specified
    model_type = model or DEFAULT_IMAGE_MODEL

    # Try the specified/default model first
    try:
        model_instance = ModelFactory.create_model(
            model_type=model_type
        )
        return model_instance.describe_image(image_path)
    except (ConnectionError, ConnectionRefusedError) as e:
        logger.warning(f"Failed to connect to {model_type}: {str(e)}")

        # If the default model fails, try other available models
        if (
            not model
        ):  # Only try alternatives if no specific model was requested
            for alt_model in ModelFactory._models.keys():
                if alt_model != model_type:
                    try:
                        logger.info(
                            f"Attempting to use alternative model: {alt_model}"
                        )
                        model_instance = ModelFactory.create_model(
                            model_type=alt_model
                        )
                        return model_instance.describe_image(image_path)
                    except (
                        ConnectionError,
                        ConnectionRefusedError,
                    ) as e:
                        logger.warning(
                            f"Failed to connect to {alt_model}: {str(e)}"
                        )
                        continue
                    except Exception as e:
                        logger.error(
                            f"Error using {alt_model}: {str(e)}"
                        )
                        continue

        # If we get here, either a specific model was requested or all alternatives failed
        raise ConnectionError(
            f"Failed to connect to {model_type} and no working alternatives found"
        )
