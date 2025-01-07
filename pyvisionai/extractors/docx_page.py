"""DOCX page-as-image extractor."""

import os
import subprocess
import tempfile
from PIL import Image
import time

from pyvisionai.extractors.base import BaseExtractor


class DocxPageImageExtractor(BaseExtractor):
    """Extract content from DOCX files by converting pages to images."""

    def convert_to_pdf(self, docx_path: str) -> str:
        """Convert DOCX to PDF using LibreOffice."""
        try:
            # Create a temporary directory for the PDF
            temp_dir = tempfile.mkdtemp()

            # Get absolute paths
            abs_docx_path = os.path.abspath(docx_path)
            abs_temp_dir = os.path.abspath(temp_dir)

            # The output PDF will have the same name as the input DOCX
            docx_filename = os.path.splitext(os.path.basename(docx_path))[0]
            pdf_path = os.path.join(abs_temp_dir, f"{docx_filename}.pdf")

            # Convert DOCX to PDF using LibreOffice
            cmd = [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                abs_temp_dir,
                abs_docx_path,
            ]

            # Run the command and capture output
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

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
            raise RuntimeError(f"Failed to convert DOCX to PDF: {str(e)}") from e

    def convert_pages_to_images(self, pdf_path: str) -> list:
        """Convert PDF pages to images using pdf2image."""
        from pdf2image import convert_from_path

        return convert_from_path(pdf_path, dpi=300)

    def save_image(self, image: Image.Image, output_dir: str, image_name: str) -> str:
        """Save an image to the output directory."""
        img_path = os.path.join(output_dir, f"{image_name}.jpg")
        image.save(img_path, "JPEG", quality=95)
        return img_path

    def extract(self, docx_path: str, output_dir: str) -> str:
        """Process DOCX file by converting each page to an image."""
        try:
            docx_filename = os.path.splitext(os.path.basename(docx_path))[0]

            # Create temporary directory for page images
            pages_dir = os.path.join(output_dir, f"{docx_filename}_pages")
            if not os.path.exists(pages_dir):
                os.makedirs(pages_dir)

            # Convert DOCX to PDF first
            pdf_path = self.convert_to_pdf(docx_path)

            # Convert PDF pages to images
            images = self.convert_pages_to_images(pdf_path)

            # Generate markdown content
            md_content = f"# {docx_filename}\n\n"

            # Process each page
            for page_num, image in enumerate(images):
                # Save page image
                image_name = f"page_{page_num + 1}"
                img_path = self.save_image(image, pages_dir, image_name)

                # Get page description using configured model
                page_description = self.describe_image(img_path)

                # Add to markdown
                md_content += f"## Page {page_num + 1}\n\n"
                md_content += f"[Image {page_num + 1}]\n"
                md_content += f"Description: {page_description}\n\n"

                # Clean up image file
                os.remove(img_path)

            # Save markdown file
            md_file_path = os.path.join(output_dir, f"{docx_filename}_docx.md")
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)

            # Clean up temporary files and directories
            os.remove(pdf_path)
            os.rmdir(os.path.dirname(pdf_path))  # Remove temp PDF directory
            os.rmdir(pages_dir)  # Remove pages directory

            return md_file_path

        except Exception as e:
            print(f"Error processing DOCX: {str(e)}")
            raise
