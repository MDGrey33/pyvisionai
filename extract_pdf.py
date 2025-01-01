"""
Extract text and images from a PDF file.
"""

import os
import fitz  # PyMuPDF
from PIL import Image
import io
from describe_image import describe_image


def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def extract_text(page):
    """Extract text from a PDF page."""
    return page.get_text()


def extract_images(page):
    """Extract images from a PDF page."""
    return page.get_images()


def convert_image(pdf_document, xref):
    """Convert an image from a PDF document."""
    base_image = pdf_document.extract_image(xref)
    image_bytes = base_image["image"]
    return Image.open(io.BytesIO(image_bytes))


def save_image(image, output_dir, image_name):
    """Save an image extracted from a PDF document."""
    img_path = os.path.join(output_dir, f"{image_name}.png")
    image.save(img_path, "PNG")
    return img_path


def process_pdf(pdf_path, output_dir):
    """Process a PDF file and extract text and images."""
    try:
        pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
        pdf_document = fitz.open(pdf_path)

        md_content = f"# {pdf_filename}\n\n"

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text_content = extract_text(page)
            image_list = extract_images(page)

            md_content += f"## Page {page_num + 1}\n\n"
            md_content += text_content + "\n\n"

            for img_index, img in enumerate(image_list):
                xref = img[0]
                image = convert_image(pdf_document, xref)
                image_name = f"{pdf_filename}_page_{page_num + 1}_image_{img_index + 1}"
                img_path = save_image(image, output_dir, image_name)
                image_description = describe_image(img_path)
                md_content += f"[Image {img_index + 1}]\n"
                md_content += f"Description: {image_description}\n\n"
                os.remove(img_path)

        pdf_document.close()

        md_file_path = os.path.join(output_dir, f"{pdf_filename}.md")
        with open(md_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(md_content)

        print(f"Markdown file generated: {md_file_path}")

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")


def process_pdf_files(pdf_folder, output_folder):
    """Process all PDF files in the specified folder."""
    create_directory_if_not_exists(pdf_folder)
    create_directory_if_not_exists(output_folder)

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"\nProcessing: {filename}")
            process_pdf(pdf_path, output_folder)


if __name__ == "__main__":
    pdf_folder = "./content/source"
    output_folder = "./content/extracted"
    process_pdf_files(pdf_folder, output_folder)
