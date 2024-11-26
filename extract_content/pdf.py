import os
import fitz  # PyMuPDF
from PIL import Image
import io

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_text(page):
    return page.get_text()

def extract_images(page):
    return page.get_images()

def convert_image(pdf_document, xref):
    base_image = pdf_document.extract_image(xref)
    image_bytes = base_image["image"]
    return Image.open(io.BytesIO(image_bytes))

def create_image_tag(pdf_filename, image_name):
    return f"##################################################\n<img>{pdf_filename}_{image_name}.png</img>\n##################################################"

def insert_image_tag(text, image_tag):
    return text + "\n" + image_tag + "\n"

def process_page(pdf_document, page_num, pdf_filename):
    page = pdf_document[page_num]
    text = extract_text(page)
    image_list = extract_images(page)
    
    images = []
    for img_index, img in enumerate(image_list):
        xref = img[0]
        image = convert_image(pdf_document, xref)
        image_name = f"image_{page_num + 1}_{img_index + 1}"
        image_tag = create_image_tag(pdf_filename, image_name)
        text = insert_image_tag(text, image_tag)
        images.append((image_name, image))
    
    return text, images

def extract_text_and_images(pdf_path, pdf_filename):
    pdf_document = fitz.open(pdf_path)
    text_content = ""
    all_images = []
    
    for page_num in range(pdf_document.page_count):
        page_text, page_images = process_page(pdf_document, page_num, pdf_filename)
        text_content += f"\n--- Page {page_num + 1} ---\n" + page_text
        all_images.extend(page_images)
    
    pdf_document.close()
    return text_content, all_images

def save_text_with_image_tags(text_content, output_dir, pdf_filename):
    text_path = os.path.join(output_dir, f"{pdf_filename}_text.txt")
    with open(text_path, "w", encoding="utf-8") as file:
        file.write(text_content)
    print(f"Text extracted and saved to: {text_path}")

def save_extracted_images(images, output_dir, pdf_filename):
    for img_name, img in images:
        img_path = os.path.join(output_dir, f"{pdf_filename}_{img_name}.png")
        img.save(img_path, "PNG")
        print(f"Image saved to: {img_path}")

def process_pdf(pdf_path, output_dir):
    try:
        pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
        text_content, images = extract_text_and_images(pdf_path, pdf_filename)
        save_text_with_image_tags(text_content, output_dir, pdf_filename)
        save_extracted_images(images, output_dir, pdf_filename)
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    pdf_folder = "./content/source"
    output_folder = "./content/extracted"
    
    create_directory_if_not_exists(pdf_folder)
    create_directory_if_not_exists(output_folder)
    
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"\nProcessing: {filename}")
            process_pdf(pdf_path, output_folder)
