"""
Extract text and images separately from PDF files using pdfminer.six and PyPDF2.
"""

import os
from io import StringIO
from typing import List, Tuple
import zlib
import re

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from PyPDF2 import PdfReader
from PIL import Image
import io

from pyvisionai.describers.ollama import describe_image_ollama as describe_image
from pyvisionai.extractors.base import BaseExtractor


def get_color_mode(color_space) -> str:
    """Determine the color mode from the PDF color space."""
    if isinstance(color_space, str):
        if color_space == "/DeviceRGB":
            return "RGB"
        elif color_space == "/DeviceCMYK":
            return "CMYK"
        elif color_space == "/DeviceGray":
            return "L"
    elif isinstance(color_space, list):
        # Handle ICC and other color spaces
        if color_space[0] == "/ICCBased":
            # Most ICC profiles are RGB or CMYK
            return "RGB"  # We'll convert to RGB as a safe default
    return "RGB"  # Default to RGB if unsure


class PDFTextImageExtractor(BaseExtractor):
    """Extract text and images separately from PDF using pdfminer.six and PyPDF2."""

    def extract_text(self, pdf_path: str, page_number: int) -> str:
        """Extract text from a specific page using pdfminer.six."""
        output_string = StringIO()
        with open(pdf_path, "rb") as in_file:
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

    def extract_images(
        self, pdf_path: str, page_number: int
    ) -> List[Tuple[bytes, str]]:
        """Extract images from a specific page using PyPDF2."""
        images = []
        reader = PdfReader(pdf_path)
        page = reader.pages[page_number]

        if "/Resources" in page and "/XObject" in page["/Resources"]:
            xObject = page["/Resources"]["/XObject"].get_object()

            for obj_name in xObject:
                obj = xObject[obj_name].get_object()
                if obj["/Subtype"] == "/Image":
                    try:
                        # Get raw data
                        data = obj.get_data()
                        
                        # Extract image data based on filter type
                        if obj["/Filter"] == "/DCTDecode":
                            # JPEG image
                            img_data = data
                            ext = "jpg"
                        elif obj["/Filter"] == "/FlateDecode":
                            # PNG image
                            width = obj["/Width"]
                            height = obj["/Height"]
                            
                            # Get color mode
                            mode = get_color_mode(obj.get("/ColorSpace", "/DeviceRGB"))
                            
                            # Calculate expected data size
                            channels = len(mode)  # RGB=3, CMYK=4, L=1
                            bits_per_component = obj.get("/BitsPerComponent", 8)
                            expected_size = width * height * channels * (bits_per_component // 8)
                            
                            # Try to decompress data if needed
                            try:
                                img_data = zlib.decompress(data)
                            except:
                                img_data = data
                            
                            # Verify data size
                            if len(img_data) != expected_size:
                                print(f"Warning: Data size mismatch. Got {len(img_data)}, expected {expected_size}")
                                continue
                            
                            # Create PIL Image from raw data
                            try:
                                img = Image.frombytes(mode, (width, height), img_data)
                                
                                # Convert to RGB if needed
                                if mode != "RGB":
                                    img = img.convert("RGB")
                                
                                # Save as PNG
                                img_byte_arr = io.BytesIO()
                                img.save(img_byte_arr, format="PNG")
                                img_data = img_byte_arr.getvalue()
                                ext = "png"
                            except Exception as e:
                                print(f"Error creating image: {str(e)}")
                                continue
                        elif obj["/Filter"] == "/JPXDecode":
                            # JPEG2000
                            img_data = data
                            ext = "jp2"
                        else:
                            print(f"Unsupported filter: {obj['/Filter']}")
                            continue

                        # Verify image data
                        try:
                            img = Image.open(io.BytesIO(img_data))
                            if img.mode != "RGB":
                                img = img.convert("RGB")
                            
                            # Check for black image
                            pixels = list(img.getdata())
                            black_pixels = sum(1 for p in pixels if p == (0, 0, 0))
                            black_percentage = (black_pixels / len(pixels)) * 100
                            if black_percentage > 90:
                                print(f"Warning: Image is {black_percentage:.1f}% black")
                                continue
                            
                            # Convert back to bytes
                            img_byte_arr = io.BytesIO()
                            img.save(img_byte_arr, format=ext.upper())
                            img_data = img_byte_arr.getvalue()
                            
                        except Exception as e:
                            print(f"Error verifying image: {str(e)}")
                            continue

                        images.append((img_data, ext))
                    except Exception as e:
                        print(f"Error extracting image: {str(e)}")
                        continue

        return images

    def save_image(
        self, image_data: bytes, output_dir: str, image_name: str, ext: str
    ) -> str:
        """Save an image to the output directory."""
        try:
            # Convert image data to PIL Image
            image = Image.open(io.BytesIO(image_data))
            # Convert to RGB if necessary
            if image.mode != "RGB":
                image = image.convert("RGB")
            # Save as JPEG (supported format)
            img_path = os.path.join(output_dir, f"{image_name}.jpg")
            image.save(img_path, "JPEG", quality=95)
            return img_path
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            raise

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
                    image_name = (
                        f"{pdf_filename}_page_{page_num + 1}_image_{img_index + 1}"
                    )
                    img_path = self.save_image(img_data, output_dir, image_name, ext)

                    # Get image description
                    image_description = describe_image(img_path)
                    md_content += f"[Image {img_index + 1}]\n"
                    md_content += f"Description: {image_description}\n\n"

                    # Clean up image file
                    os.remove(img_path)

            # Save markdown file
            md_file_path = os.path.join(output_dir, f"{pdf_filename}_pdf.md")
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)

            return md_file_path

        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            raise
