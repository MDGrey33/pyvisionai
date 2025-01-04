"""
Extract content from PDF files by converting each page to an image.
"""

import os
import fitz  # PyMuPDF
from PIL import Image
from describe_image import describe_image
from pdf_extractors.pdf_extractor_base import PDFExtractor


def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


class PDFPageImageExtractor(PDFExtractor):
    """Extract content by converting each page to an image."""

    def convert_page_to_image(self, page, dpi=300):
        """Convert a PDF page to an image."""
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img

    def save_image(self, image, output_dir, image_name):
        """Save an image to the output directory."""
        img_path = os.path.join(output_dir, f"{image_name}.png")
        image.save(img_path, "PNG")
        return img_path

    def extract(self, pdf_path: str, output_dir: str) -> str:
        """Process PDF file by converting each page to an image."""
        try:
            pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
            pdf_document = fitz.open(pdf_path)

            # Create temporary directory for page images
            pages_dir = os.path.join(output_dir, f"{pdf_filename}_pages")
            create_directory_if_not_exists(pages_dir)

            # Generate markdown content
            md_content = f"# {pdf_filename}\n\n"

            # Process each page
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                
                # Convert page to image
                page_image = self.convert_page_to_image(page)
                
                # Save page image
                image_name = f"page_{page_num + 1}"
                img_path = self.save_image(page_image, pages_dir, image_name)
                
                # Get page description
                page_description = describe_image(img_path)
                
                # Add to markdown
                md_content += f"## Page {page_num + 1}\n\n"
                md_content += f"[Image {page_num + 1}]\n"
                md_content += f"Description: {page_description}\n\n"
                
                # Clean up image file
                os.remove(img_path)

            pdf_document.close()

            # Save markdown file
            md_file_path = os.path.join(output_dir, f"{pdf_filename}.md")
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)

            # Clean up pages directory
            os.rmdir(pages_dir)

            return md_file_path

        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            raise 