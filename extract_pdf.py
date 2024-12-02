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


def save_extracted_images(images, output_dir, pdf_filename):
    """Save extracted images from a PDF document."""
    for img_name, img in images:
        img_path = os.path.join(output_dir, f"{pdf_filename}_{img_name}.png")
        img.save(img_path, "PNG")
        print(f"Image saved to: {img_path}")


def create_image_tag(pdf_filename, image_name):
    """Create an image tag for a PDF image."""
    separator = "#" * 50
    return f"{separator}\n<img>{pdf_filename}_{image_name}.png</img>\n{separator}"


def insert_image_tag(text, image_tag):
    """Insert an image tag into the text."""
    return text + "\n" + image_tag + "\n"


def process_page(pdf_document, page_num, pdf_filename, output_dir):
    """Process a PDF page and extract text and images."""
    page = pdf_document[page_num]
    text = extract_text(page)
    image_list = extract_images(page)

    images = []
    for img_index, img in enumerate(image_list):
        xref = img[0]
        image = convert_image(pdf_document, xref)
        image_name = f"image_{page_num + 1}_{img_index + 1}"

        # Save the image immediately
        img_path = os.path.join(output_dir, f"{pdf_filename}_{image_name}.png")
        image.save(img_path, "PNG")
        print(f"Image saved to: {img_path}")

        # Get the image description
        image_description = describe_image(img_path)
        print(f"Image description generated")

        # Create image tag with description
        image_tag = (
            create_image_tag(pdf_filename, image_name)
            + f"\nDescription: {image_description}\n"
            + "#" * 50
            + "\n"
        )

        text = insert_image_tag(text, image_tag)
        images.append((image_name, image))

    return text, images


def extract_text_and_images(pdf_path, pdf_filename, output_dir):
    """Extract text and images from a PDF document."""
    pdf_document = fitz.open(pdf_path)
    text_content = ""
    all_images = []

    for page_num in range(pdf_document.page_count):
        page_text, page_images = process_page(
            pdf_document, page_num, pdf_filename, output_dir
        )
        text_content += f"\n--- Page {page_num + 1} ---\n" + page_text
        all_images.extend(page_images)

    pdf_document.close()
    return text_content, all_images


def save_text_with_image_tags(text_content, output_dir, pdf_filename):
    """Save the extracted text with image tags to a file."""
    text_path = os.path.join(output_dir, f"{pdf_filename}_text.txt")
    with open(text_path, "w", encoding="utf-8") as file:
        file.write(text_content)
    print(f"Text extracted and saved to: {text_path}")


def process_pdf(pdf_path, output_dir):
    """Process a PDF file and extract text and images."""
    try:
        pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
        text_content, images = extract_text_and_images(
            pdf_path, pdf_filename, output_dir
        )
        save_text_with_image_tags(text_content, output_dir, pdf_filename)
        # No need to save images again here as they are already saved in process_page
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
