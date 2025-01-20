"""PPTX page-as-image extractor.

Converts PPTX files to images by first converting to PDF using LibreOffice,
then converting PDF pages to images using pdf2image."""

import concurrent.futures
import logging
import os
import subprocess
import tempfile
import time
from dataclasses import dataclass

from PIL import Image

from pyvisionai.extractors.base import BaseExtractor

logger = logging.getLogger(__name__)


@dataclass
class SlideTask:
    """Container for slide processing task data."""

    image: Image.Image
    image_name: str
    output_dir: str
    index: int


class PptxPageImageExtractor(BaseExtractor):
    """Extract content from PPTX files by converting slides to images.

    Uses LibreOffice to convert PPTX to PDF, then pdf2image to convert
    PDF pages to images. Each slide is processed in parallel to generate
    descriptions."""

    def convert_to_pdf(self, pptx_path: str) -> str:
        """Convert PPTX to PDF using LibreOffice."""
        try:
            # Create a temporary directory for the PDF
            temp_dir = tempfile.mkdtemp()

            # Get absolute paths
            abs_pptx_path = os.path.abspath(pptx_path)
            abs_temp_dir = os.path.abspath(temp_dir)

            # The output PDF will have the same name as the input PPTX
            pptx_filename = os.path.splitext(
                os.path.basename(pptx_path)
            )[0]
            pdf_path = os.path.join(
                abs_temp_dir, f"{pptx_filename}.pdf"
            )

            # Convert PPTX to PDF using LibreOffice
            cmd = [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                abs_temp_dir,
                abs_pptx_path,
            ]

            # Run the command and capture output
            result = subprocess.run(
                cmd, check=True, capture_output=True, text=True
            )

            # Wait a moment for the file to be written
            time.sleep(1)

            # Verify the PDF was created
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(
                    f"PDF file was not created. LibreOffice output:\n"
                    f"STDOUT: {result.stdout}\n"
                    f"STDERR: {result.stderr}"
                )

            return pdf_path

        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"LibreOffice conversion failed:\n"
                f"STDOUT: {e.stdout}\n"
                f"STDERR: {e.stderr}"
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Failed to convert PPTX to PDF: {str(e)}"
            ) from e

    def convert_pages_to_images(self, pdf_path: str) -> list:
        """Convert PDF pages to images using pdf2image."""
        from pdf2image import convert_from_path

        return convert_from_path(pdf_path, dpi=300)

    def save_image(
        self, image: Image.Image, output_dir: str, image_name: str
    ) -> str:
        """Save an image to the output directory."""
        img_path = os.path.join(output_dir, f"{image_name}.jpg")
        image.save(img_path, "JPEG", quality=95)
        return img_path

    def process_slide(self, task: SlideTask) -> tuple[int, str]:
        """Process a single slide.

        Saves the slide as an image, generates a description using the configured
        model, then cleans up the image file.

        Args:
            task: SlideTask containing the slide image and processing details

        Returns:
            Tuple of (slide index, description)
        """
        try:
            # Save slide image
            img_path = self.save_image(
                task.image, task.output_dir, task.image_name
            )

            # Get slide description using configured model
            slide_description = self.describe_image(img_path)

            # Clean up image file
            os.remove(img_path)

            return task.index, slide_description
        except Exception as e:
            logger.error(
                f"Error processing slide {task.image_name}: {str(e)}"
            )
            return (
                task.index,
                f"Error: Could not process slide {task.image_name}",
            )

    def extract(self, pptx_path: str, output_dir: str) -> str:
        """Process PPTX file by converting each slide to an image."""
        try:
            logger.info("Processing PPTX file...")

            pptx_filename = os.path.splitext(
                os.path.basename(pptx_path)
            )[0]

            # Create temporary directory for slide images
            slides_dir = os.path.join(
                output_dir, f"{pptx_filename}_slides"
            )
            if not os.path.exists(slides_dir):
                os.makedirs(slides_dir)

            # Convert PPTX to PDF first
            pdf_path = self.convert_to_pdf(pptx_path)
            logger.info("Converted PPTX to PDF")

            # Convert PDF pages to images
            images = self.convert_pages_to_images(pdf_path)
            logger.info(f"Converting {len(images)} slides to images")

            # Generate markdown content
            md_content = f"# {pptx_filename}\n\n"

            # Create slide tasks
            slide_tasks = []
            for slide_num, image in enumerate(images):
                image_name = f"slide_{slide_num + 1}"
                task = SlideTask(
                    image=image,
                    image_name=image_name,
                    output_dir=slides_dir,
                    index=slide_num,
                )
                slide_tasks.append(task)

            # Process slides in parallel
            descriptions = [""] * len(slide_tasks)
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=4
            ) as executor:
                # Submit all tasks
                future_to_task = {
                    executor.submit(self.process_slide, task): task
                    for task in slide_tasks
                }

                # Collect results as they complete
                for future in concurrent.futures.as_completed(
                    future_to_task
                ):
                    idx, description = future.result()
                    descriptions[idx] = description

            # Add descriptions to markdown in correct order
            for slide_num, description in enumerate(descriptions):
                md_content += f"## Slide {slide_num + 1}\n\n"
                md_content += f"[Image {slide_num + 1}]\n"
                md_content += f"Description: {description}\n\n"

            # Save markdown file
            md_file_path = os.path.join(
                output_dir, f"{pptx_filename}_pptx.md"
            )
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)

            # Clean up temporary files
            os.remove(pdf_path)
            os.rmdir(
                os.path.dirname(pdf_path)
            )  # Remove temp PDF directory
            os.rmdir(slides_dir)  # Remove slides directory

            logger.info("PPTX processing completed successfully")
            return md_file_path

        except Exception as e:
            logger.error(f"Error processing PPTX: {str(e)}")
            raise
