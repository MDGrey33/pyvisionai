"""
Extract content from PDF files by converting each page to an image using pdf2image.
"""

import os
from pdf2image import convert_from_path
from describe_image import describe_image
from pdf_extractors.pdf_extractor_base import PDFExtractor


class PDFPageImageExtractorV2(PDFExtractor):
    """Extract content by converting each page to an image using pdf2image."""

    def convert_pages_to_images(self, pdf_path: str, dpi=300):
        """Convert PDF pages to images."""
        return convert_from_path(pdf_path, dpi=dpi)

    def save_image(self, image, output_dir: str, image_name: str) -> str:
        """Save an image to the output directory."""
        img_path = os.path.join(output_dir, f"{image_name}.png")
        image.save(img_path, "PNG")
        return img_path

    def extract(self, pdf_path: str, output_dir: str) -> str:
        """Process PDF file by converting each page to an image."""
        try:
            pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]

            # Create temporary directory for page images
            pages_dir = os.path.join(output_dir, f"{pdf_filename}_pages")
            if not os.path.exists(pages_dir):
                os.makedirs(pages_dir)

            # Convert PDF pages to images
            images = self.convert_pages_to_images(pdf_path)

            # Generate markdown content
            md_content = f"# {pdf_filename}\n\n"

            # Process each page
            for page_num, image in enumerate(images):
                # Save page image
                image_name = f"page_{page_num + 1}"
                img_path = self.save_image(image, pages_dir, image_name)
                
                # Get page description
                page_description = describe_image(img_path)
                
                # Add to markdown
                md_content += f"## Page {page_num + 1}\n\n"
                md_content += f"[Image {page_num + 1}]\n"
                md_content += f"Description: {page_description}\n\n"
                
                # Clean up image file
                os.remove(img_path)

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