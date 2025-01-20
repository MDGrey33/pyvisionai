"""Extract text and images separately from PDF files using pdfminer.six and pypdf.

This module provides functionality to extract both text and images from PDF files,
processing them page by page and combining the results into a markdown file.

Key Features:
- Text extraction using pdfminer.six for accurate text content
- Image extraction using PyPDF2 for various image formats (JPEG, PNG, JPEG2000)
- Image format conversion and validation
- Automatic image description generation
- Markdown output generation with interleaved text and images

Implementation Notes:
- Uses sequential processing for image extraction within pages rather than parallel
  processing. Testing showed that parallel image processing within pages actually
  decreased performance due to:
  1. The overhead of thread creation/management exceeded benefits for typical
     number of images per page (usually 1-3 images)
  2. The image description API calls being the main bottleneck, which doesn't
     benefit from local parallelization
  3. Additional memory overhead from holding multiple images in memory

Classes:
    PDFTextImageExtractor: Main class for extracting text and images from PDFs

Dependencies:
    - pdfminer.six: For text extraction
    - PyPDF2: For image extraction
    - Pillow: For image processing
"""

import concurrent.futures
import io
import os
import re
import zlib
from dataclasses import dataclass
from io import StringIO
from typing import List, Tuple

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from PIL import Image
from pypdf import PdfReader

from pyvisionai.extractors.base import BaseExtractor
from pyvisionai.utils.logger import logger


@dataclass
class PageTask:
    """Task for processing a single page."""

    page_num: int
    pdf_path: str
    output_dir: str
    filename: str


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
            device = TextConverter(
                rsrcmgr, output_string, laparams=LAParams()
            )
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
                            mode = get_color_mode(
                                obj.get("/ColorSpace", "/DeviceRGB")
                            )

                            # Calculate expected data size
                            channels = len(mode)  # RGB=3, CMYK=4, L=1
                            bits_per_component = obj.get(
                                "/BitsPerComponent", 8
                            )
                            expected_size = (
                                width
                                * height
                                * channels
                                * (bits_per_component // 8)
                            )

                            # Try to decompress data if needed
                            try:
                                img_data = zlib.decompress(data)
                            except zlib.error:
                                # If decompression fails, use raw data
                                img_data = data

                            # Verify data size
                            if len(img_data) != expected_size:
                                logger.warning(
                                    f"Warning: Data size mismatch. Got {len(img_data)}, expected {expected_size}"
                                )
                                continue

                            # Create PIL Image from raw data
                            try:
                                img = Image.frombytes(
                                    mode, (width, height), img_data
                                )

                                # Convert to RGB if needed
                                if mode != "RGB":
                                    img = img.convert("RGB")

                                # Save as PNG
                                img_byte_arr = io.BytesIO()
                                img.save(img_byte_arr, format="PNG")
                                img_data = img_byte_arr.getvalue()
                                ext = "png"
                            except Exception as e:
                                logger.error(
                                    f"Error creating image: {str(e)}"
                                )
                                continue
                        elif obj["/Filter"] == "/JPXDecode":
                            # JPEG2000
                            img_data = data
                            ext = "jp2"
                        else:
                            logger.warning(
                                f"Unsupported filter: {obj['/Filter']}"
                            )
                            continue

                        # Verify image data
                        try:
                            img = Image.open(io.BytesIO(img_data))
                            if img.mode != "RGB":
                                img = img.convert("RGB")

                            # Check for black image
                            pixels = list(img.getdata())
                            black_pixels = sum(
                                1 for p in pixels if p == (0, 0, 0)
                            )
                            black_percentage = (
                                black_pixels / len(pixels)
                            ) * 100
                            if black_percentage > 90:
                                logger.warning(
                                    f"Warning: Image is {black_percentage:.1f}% black"
                                )
                                continue

                            # Convert back to bytes
                            img_byte_arr = io.BytesIO()
                            img.save(img_byte_arr, format=ext.upper())
                            img_data = img_byte_arr.getvalue()

                        except Exception as e:
                            logger.error(
                                f"Error verifying image: {str(e)}"
                            )
                            continue

                        images.append((img_data, ext))
                    except Exception as e:
                        logger.error(
                            f"Error extracting image: {str(e)}"
                        )
                        continue

        return images

    def save_image(
        self,
        image_data: bytes,
        output_dir: str,
        image_name: str,
        ext: str,
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
            logger.error(f"Error saving image: {str(e)}")
            raise

    def process_page(self, task: PageTask) -> tuple[int, str]:
        """Process a single page, extracting text and images."""
        try:
            # Extract text
            text_content = self.extract_text(
                task.pdf_path, task.page_num
            )

            # Extract images
            images = self.extract_images(task.pdf_path, task.page_num)

            # Build page content
            page_content = (
                f"## Page {task.page_num + 1}\n\n{text_content}\n\n"
            )

            # Process images for this page
            for img_index, (img_data, ext) in enumerate(images):
                image_name = f"{task.filename}_page_{task.page_num + 1}_image_{img_index + 1}"
                img_path = self.save_image(
                    img_data, task.output_dir, image_name, ext
                )

                # Get image description using base class method
                image_description = self.describe_image(img_path)
                page_content += f"[Image {img_index + 1}]\n"
                page_content += f"Description: {image_description}\n\n"

                # Clean up image file
                os.remove(img_path)

            return task.page_num, page_content
        except Exception as e:
            logger.error(
                f"Error processing page {task.page_num + 1}: {str(e)}"
            )
            return (
                task.page_num,
                f"Error: Could not process page {task.page_num + 1}\n\n",
            )

    def extract(self, pdf_path: str, output_dir: str) -> str:
        """Process PDF file by extracting text and images separately."""
        try:
            pdf_filename = os.path.splitext(os.path.basename(pdf_path))[
                0
            ]
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)

            md_content = f"# {pdf_filename}\n\n"

            # Create page tasks
            page_tasks = [
                PageTask(
                    page_num=i,
                    pdf_path=pdf_path,
                    output_dir=output_dir,
                    filename=pdf_filename,
                )
                for i in range(num_pages)
            ]

            # Process pages in parallel
            results = [""] * num_pages
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=4
            ) as executor:
                # Submit all tasks
                future_to_page = {
                    executor.submit(
                        self.process_page, task
                    ): task.page_num
                    for task in page_tasks
                }

                # Collect results as they complete
                for future in concurrent.futures.as_completed(
                    future_to_page
                ):
                    page_num, page_content = future.result()
                    results[page_num] = page_content

            # Add all pages to markdown in correct order
            md_content += "".join(results)

            # Save markdown file
            md_file_path = os.path.join(
                output_dir, f"{pdf_filename}_pdf.md"
            )
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_content)

            # For status/info messages
            logger.info("Processing PDF file...")
            logger.info("PDF processing completed successfully")

            return md_file_path

        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise
