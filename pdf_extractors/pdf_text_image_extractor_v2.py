"""
Extract text and images separately from PDF files using pdfminer.six and PyPDF2.
"""

import os
from io import StringIO
from typing import List, Tuple

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from PyPDF2 import PdfReader
from PIL import Image
import io

from describe_image import describe_image
from pdf_extractors.pdf_extractor_base import PDFExtractor


class PDFTextImageExtractorV2(PDFExtractor):
    """Extract text and images separately from PDF using pdfminer.six and PyPDF2."""

    def extract_text(self, pdf_path: str, page_number: int) -> str:
        """Extract text from a specific page using pdfminer.six."""
        output_string = StringIO()
        with open(pdf_path, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            
            # Get specific page
            for i, page in enumerate(PDFPage.create_pages(doc)):
                if i == page_number:
                    interpreter.process_page(page)
                    break
                    
        return output_string.getvalue()

    def extract_images(self, pdf_path: str, page_number: int) -> List[Tuple[bytes, str]]:
        """Extract images from a specific page using PyPDF2."""
        images = []
        reader = PdfReader(pdf_path)
        page = reader.pages[page_number]
        
        if '/Resources' in page and '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].get_object()
            
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    image = xObject[obj]
                    
                    # Try to extract image data
                    try:
                        if image['/Filter'] == '/DCTDecode':
                            # JPEG image
                            img_data = image._data
                            ext = 'jpg'
                        elif image['/Filter'] == '/FlateDecode':
                            # PNG image
                            img_data = image._data
                            ext = 'png'
                        elif image['/Filter'] == '/JPXDecode':
                            # JPEG2000 image
                            img_data = image._data
                            ext = 'jp2'
                        else:
                            continue
                            
                        images.append((img_data, ext))
                    except Exception as e:
                        print(f"Error extracting image: {str(e)}")
                        continue
                        
        return images

    def save_image(self, image_data: bytes, output_dir: str, image_name: str, ext: str) -> str:
        """Save an image to the output directory."""
        img_path = os.path.join(output_dir, f"{image_name}.{ext}")
        with open(img_path, 'wb') as img_file:
            img_file.write(image_data)
        return img_path

    def extract(self, pdf_path: str, output_dir: str) -> str:
        """Process PDF file by extracting text and images separately."""
        try:
            pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)

            md_content = f"# {pdf_filename}\n\n"

            for page_num in range(num_pages):
                # Extract text
                text_content = self.extract_text(pdf_path, page_num)
                md_content += f"## Page {page_num + 1}\n\n"
                md_content += text_content + "\n\n"

                # Extract images
                images = self.extract_images(pdf_path, page_num)
                for img_index, (img_data, ext) in enumerate(images):
                    image_name = f"{pdf_filename}_page_{page_num + 1}_image_{img_index + 1}"
                    img_path = self.save_image(img_data, output_dir, image_name, ext)
                    
                    # Get image description
                    image_description = describe_image(img_path)
                    md_content += f"[Image {img_index + 1}]\n"
                    md_content += f"Description: {image_description}\n\n"
                    
                    # Clean up image file
                    os.remove(img_path)

            # Save markdown file
            md_file_path = os.path.join(output_dir, f"{pdf_filename}.md")
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)

            return md_file_path

        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            raise 