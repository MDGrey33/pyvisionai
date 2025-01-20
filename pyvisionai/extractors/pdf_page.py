"""PDF page-as-image extractor."""

import concurrent.futures
import logging
import os
from typing import Tuple

from pdf2image import convert_from_path
from PIL import Image

from pyvisionai.extractors.base import BaseExtractor

logger = logging.getLogger(__name__)


class PDFPageImageExtractor(BaseExtractor):
    """Extract content from PDF files by converting pages to images."""

    def convert_pages_to_images(self, pdf_path: str) -> list:
        """Convert PDF pages to images."""
        return convert_from_path(pdf_path, dpi=300)

    def save_image(
        self, image: Image.Image, output_dir: str, image_name: str
    ) -> str:
        """Save an image to the output directory."""
        img_path = os.path.join(output_dir, f"{image_name}.jpg")
        image.save(img_path, "JPEG", quality=95)
        return img_path

    def process_page(
        self, page_data: Tuple[int, Image.Image], pages_dir: str
    ) -> Tuple[int, str]:
        """Process a single page.

        Args:
            page_data: Tuple of (page number, page image)
            pages_dir: Directory to save page images

        Returns:
            Tuple of (page number, page description)
        """
        try:
            page_num, image = page_data
            # Save page image
            image_name = f"page_{page_num + 1}"
            img_path = self.save_image(image, pages_dir, image_name)

            # Get page description using configured model
            page_description = self.describe_image(img_path)

            # Clean up image file
            os.remove(img_path)

            return page_num, page_description
        except Exception as e:
            logger.error(
                f"Error processing page {page_num + 1}: {str(e)}"
            )
            return (
                page_num,
                f"Error: Could not process page {page_num + 1}",
            )

    def extract(self, pdf_path: str, output_dir: str) -> str:
        """Process PDF file by converting each page to an image."""
        try:
            pdf_filename = os.path.splitext(os.path.basename(pdf_path))[
                0
            ]

            # Create temporary directory for page images
            pages_dir = os.path.join(
                output_dir, f"{pdf_filename}_pages"
            )
            if not os.path.exists(pages_dir):
                os.makedirs(pages_dir)

            logger.info("Processing PDF file...")
            # Convert PDF pages to images
            images = self.convert_pages_to_images(pdf_path)
            logger.info(f"Converting {len(images)} pages to images")

            # Generate markdown content
            md_content = f"# {pdf_filename}\n\n"

            # Process pages in parallel
            descriptions = [""] * len(images)
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=4
            ) as executor:
                # Create page tasks
                page_tasks = [(i, img) for i, img in enumerate(images)]

                # Submit all tasks
                future_to_page = {
                    executor.submit(
                        self.process_page, task, pages_dir
                    ): task[0]
                    for task in page_tasks
                }

                # Collect results as they complete
                for future in concurrent.futures.as_completed(
                    future_to_page
                ):
                    page_num, description = future.result()
                    descriptions[page_num] = description

            # Add descriptions to markdown in correct order
            for page_num, description in enumerate(descriptions):
                md_content += f"## Page {page_num + 1}\n\n"
                md_content += f"[Image {page_num + 1}]\n"
                md_content += f"Description: {description}\n\n"

            # Save markdown file
            md_file_path = os.path.join(
                output_dir, f"{pdf_filename}_pdf.md"
            )
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)

            # Clean up pages directory after all pages are processed
            os.rmdir(pages_dir)

            logger.info("PDF processing completed successfully")
            return md_file_path

        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise
