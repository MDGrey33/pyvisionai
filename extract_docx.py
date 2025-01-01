"""
Extract text and images from a DOCX file.
"""

import os
import docx
from docx import Document
from PIL import Image
import io
from describe_image import describe_image


def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def extract_text(doc):
    """Extract text from a DOCX document."""
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


def extract_images(doc):
    """Extract images from a DOCX document."""
    images = []
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image_data = rel.target_part.blob
            images.append(image_data)
    return images


def save_image(image_data, output_dir, docx_filename, image_index):
    """Save an image extracted from a DOCX document."""
    image = Image.open(io.BytesIO(image_data))
    image_name = f"{docx_filename}_image_{image_index}.png"
    img_path = os.path.join(output_dir, image_name)
    image.save(img_path, "PNG")
    return img_path


def process_docx(docx_path, output_dir):
    """Process a DOCX file and extract text and images."""
    try:
        docx_filename = os.path.splitext(os.path.basename(docx_path))[0]
        doc = Document(docx_path)

        text_content = extract_text(doc)
        image_data_list = extract_images(doc)

        md_content = f"# {docx_filename}\n\n"
        md_content += text_content + "\n\n"

        for index, image_data in enumerate(image_data_list):
            img_path = save_image(image_data, output_dir, docx_filename, index + 1)
            image_description = describe_image(img_path)
            md_content += f"[Image {index + 1}]\n"
            md_content += f"Description: {image_description}\n\n"

            # Delete the temporary image file
            os.remove(img_path)

        md_file_path = os.path.join(output_dir, f"{docx_filename}.md")
        with open(md_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(md_content)

        print(f"Markdown file generated: {md_file_path}")

    except Exception as e:
        print(f"Error processing DOCX: {str(e)}")


def process_docx_files(docx_folder, output_folder):
    """Process all DOCX files in the specified folder."""
    create_directory_if_not_exists(docx_folder)
    create_directory_if_not_exists(output_folder)

    for filename in os.listdir(docx_folder):
        if filename.lower().endswith(".docx"):
            docx_path = os.path.join(docx_folder, filename)
            print(f"\nProcessing: {filename}")
            process_docx(docx_path, output_folder)


if __name__ == "__main__":
    docx_folder = "./content/source"
    output_folder = "./content/extracted"
    process_docx_files(docx_folder, output_folder)
