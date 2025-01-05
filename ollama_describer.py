"""
Describer implementation using Ollama's local models.
"""

import os
import ollama
from PIL import Image
import io
import base64


class OllamaDescriber:
    """A class to generate descriptions for images using Ollama's local models."""

    def __init__(self, model="llama3.2-vision"):
        """Initialize the OllamaDescriber with the specified model."""
        self.model = model

    def _encode_image_base64(self, image_path):
        """Convert an image to base64 encoding."""
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Convert to JPEG format in memory
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            image_bytes = buffer.getvalue()
            
            # Encode to base64
            return base64.b64encode(image_bytes).decode('utf-8')

    def describe(self, image_path):
        """
        Generate a description for the image using Ollama's model.

        Args:
            image_path (str): Path to the image file.

        Returns:
            str: Description of the image.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        try:
            # Encode image to base64
            image_base64 = self._encode_image_base64(image_path)

            # Create the prompt
            prompt = "Please describe this image in detail, focusing on the main elements and their relationships."

            # Generate description using Ollama
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                images=[image_base64]
            )

            # Extract and return the description
            return response['response'].strip()

        except Exception as e:
            raise Exception(f"Error generating description with Ollama: {str(e)}")
