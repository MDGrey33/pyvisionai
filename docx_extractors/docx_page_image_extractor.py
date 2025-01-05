"""
Extract content from DOCX files by converting each page to an image.
"""

import os
import tempfile
import subprocess
from pdf2image import convert_from_path
from describe_image import describe_image
from .docx_extractor_base import DocxExtractor


def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


class DocxPageImageExtractor(DocxExtractor):
    """Extract content by converting each page to an image."""

    def convert_docx_to_pdf(self, docx_path: str, pdf_path: str):
        """Convert DOCX to PDF using LibreOffice."""
        try:
            cmd = [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                os.path.dirname(pdf_path),
                docx_path,
            ]
            subprocess.run(cmd, check=True, capture_output=True)

            # LibreOffice keeps the original filename, just changes extension
            original_pdf = os.path.join(
                os.path.dirname(pdf_path),
                os.path.splitext(os.path.basename(docx_path))[0] + ".pdf",
            )
            if original_pdf != pdf_path:
                os.rename(original_pdf, pdf_path)

        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to convert DOCX to PDF: {e.stderr.decode()}")

    def convert_pages_to_images(self, docx_path: str, output_dir: str) -> list:
        """Convert DOCX pages to images by first converting to PDF."""
        try:
            # Create temporary directory for PDF
            with tempfile.TemporaryDirectory() as temp_dir:
                # Convert DOCX to PDF
                pdf_path = os.path.join(temp_dir, "temp.pdf")
                self.convert_docx_to_pdf(docx_path, pdf_path)

                # Convert PDF pages to images
                images = convert_from_path(pdf_path)

                # Save images to output directory
                image_paths = []
                for i, image in enumerate(images, start=1):
                    image_path = os.path.join(output_dir, f"page_{i}.png")
                    image.save(image_path, "PNG")
                    image_paths.append(image_path)

                return image_paths

        except Exception as e:
            raise Exception(f"Error during page conversion: {str(e)}")

    def extract(self, docx_path: str, output_dir: str) -> str:
        """Process DOCX file by converting each page to an image."""
        try:
            docx_filename = os.path.splitext(os.path.basename(docx_path))[0]

            # Create temporary directory for page images
            pages_dir = os.path.join(output_dir, "pages")
            create_directory_if_not_exists(pages_dir)

            # Convert pages to images
            image_paths = self.convert_pages_to_images(docx_path, pages_dir)

            # Generate markdown content
            md_content = f"# {docx_filename}\n\n"

            # Process each page
            for i, image_path in enumerate(image_paths, 1):
                # Get page description
                page_description = describe_image(image_path)

                # Add to markdown
                md_content += f"## Page {i}\n\n"
                md_content += f"[Image {i}]\n"
                md_content += f"Description: {page_description}\n\n"

                # Clean up image file
                os.remove(image_path)

            # Save markdown file
            md_file_path = os.path.join(output_dir, f"{docx_filename}.md")
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)

            # Clean up pages directory
            os.rmdir(pages_dir)

            return md_file_path

        except Exception as e:
            print(f"Error processing DOCX: {str(e)}")
            raise
