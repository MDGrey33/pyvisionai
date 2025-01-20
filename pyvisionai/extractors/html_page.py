"""HTML page-as-image extractor."""

import io
import os
import tempfile

from PIL import Image

from pyvisionai.config.html_config import DEFAULT_CONFIG
from pyvisionai.extractors.base import BaseExtractor
from pyvisionai.extractors.html.browser import capture_webpage
from pyvisionai.utils.logger import logger


class HtmlPageImageExtractor(BaseExtractor):
    """Extract content from HTML files by converting pages to images."""

    def save_image(
        self, image_data: bytes, output_dir: str, image_name: str
    ) -> str:
        """Save an image to the output directory."""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            # Convert to RGB if necessary
            if image.mode != "RGB":
                image = image.convert("RGB")
            # Save as JPEG
            img_path = os.path.join(output_dir, f"{image_name}.jpg")
            image.save(img_path, "JPEG", quality=95)
            return img_path
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            raise

    def extract(self, html_path: str, output_dir: str) -> str:
        """Process HTML file by converting to image."""
        try:
            html_filename = os.path.splitext(
                os.path.basename(html_path)
            )[0]

            # Create temporary directory for page images
            pages_dir = os.path.join(
                output_dir, f"{html_filename}_pages"
            )
            if not os.path.exists(pages_dir):
                os.makedirs(pages_dir)

            # Read HTML file content
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            # Create temporary HTML file with absolute paths
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".html", delete=False
            ) as temp_html:
                # Convert relative paths to absolute
                base_dir = os.path.dirname(os.path.abspath(html_path))
                html_content = html_content.replace(
                    'src="', f'src="{base_dir}/'
                )
                html_content = html_content.replace(
                    "src='", f"src='{base_dir}/"
                )
                temp_html.write(html_content)
                temp_path = temp_html.name

            try:
                # Capture webpage as image
                screenshot = capture_webpage(
                    f"file://{temp_path}", DEFAULT_CONFIG
                )

                # Save screenshot
                image_name = "page_1"
                img_path = self.save_image(
                    screenshot, pages_dir, image_name
                )

                # Get page description using configured model
                page_description = self.describe_image(img_path)

                # Generate markdown content
                md_content = f"# {html_filename}\n\n"
                md_content += "## Page 1\n\n"
                md_content += "[Image 1]\n"
                md_content += f"Description: {page_description}\n\n"

                # Save markdown file
                md_file_path = os.path.join(
                    output_dir, f"{html_filename}_html.md"
                )
                with open(
                    md_file_path, "w", encoding="utf-8"
                ) as md_file:
                    md_file.write(md_content)

                # Clean up image file
                os.remove(img_path)

                logger.info("Processing HTML file...")
                logger.info(f"Extracted content and saved to markdown")
                logger.info("HTML processing completed successfully")

                return md_file_path

            finally:
                # Clean up temporary HTML file
                os.remove(temp_path)
                # Clean up pages directory
                os.rmdir(pages_dir)

        except Exception as e:
            logger.error(f"Error processing HTML: {str(e)}")
            raise
