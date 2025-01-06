"""DOCX content extractor."""

import os
from docx import Document
from PIL import Image
import io

from pyvisionai.extractors.base import BaseExtractor


class DocxTextImageExtractor(BaseExtractor):
    """Extract text and images from DOCX files."""

    def save_image(self, image_data: bytes, output_dir: str, image_name: str) -> str:
        """Save an image to the output directory."""
        try:
            # Convert image data to PIL Image
            image = Image.open(io.BytesIO(image_data))
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            # Save as JPEG (supported format)
            img_path = os.path.join(output_dir, f"{image_name}.jpg")
            image.save(img_path, "JPEG", quality=95)
            return img_path
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            raise

    def extract(self, docx_path: str, output_dir: str) -> str:
        """Process DOCX file by extracting text and images."""
        try:
            docx_filename = os.path.splitext(os.path.basename(docx_path))[0]
            doc = Document(docx_path)

            # Generate markdown content
            md_content = f"# {docx_filename}\n\n"

            # Process paragraphs and images
            image_count = 0
            for paragraph in doc.paragraphs:
                # Extract text
                if paragraph.text.strip():
                    md_content += f"{paragraph.text}\n\n"

                # Extract images from runs
                for run in paragraph.runs:
                    for shape in run._element.findall('.//w:drawing/wp:inline/a:graphic/a:graphicData/pic:pic/pic:blipFill/a:blip', run._element.nsmap):
                        image_rid = shape.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        if image_rid:
                            image_part = doc.part.related_parts[image_rid]
                            image_data = image_part.blob
                            image_count += 1
                            image_name = f"{docx_filename}_image_{image_count}"
                            img_path = self.save_image(image_data, output_dir, image_name)
                            
                            # Get image description using configured model
                            image_description = self.describe_image(img_path)
                            md_content += f"[Image {image_count}]\n"
                            md_content += f"Description: {image_description}\n\n"
                            
                            # Clean up image file
                            os.remove(img_path)

            # Save markdown file
            md_file_path = os.path.join(output_dir, f"{docx_filename}.md")
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)

            return md_file_path

        except Exception as e:
            print(f"Error processing DOCX: {str(e)}")
            raise 