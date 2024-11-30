import os
from docx import Document
from PIL import Image
import io
from describe_image import describe_image

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_text(doc):
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_images(doc):
    images = []
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image_data = rel.target_part.blob
            images.append(image_data)
    return images

def save_image(image_data, output_dir, docx_filename, image_index):
    image = Image.open(io.BytesIO(image_data))
    image_name = f"{docx_filename}_image_{image_index}.png"
    img_path = os.path.join(output_dir, image_name)
    image.save(img_path, "PNG")
    return img_path

def process_docx(docx_path, output_dir):
    try:
        docx_filename = os.path.splitext(os.path.basename(docx_path))[0]
        doc = Document(docx_path)
        
        text_content = extract_text(doc)
        image_data_list = extract_images(doc)
        
        for index, image_data in enumerate(image_data_list):
            img_path = save_image(image_data, output_dir, docx_filename, index + 1)
            image_description = describe_image(img_path)
            image_tag = f"Image: {img_path}\nDescription: {image_description}\n" + "#"*50 + "\n"
            text_content += "\n" + image_tag
        
        save_text_with_image_tags(text_content, output_dir, docx_filename)
        
    except Exception as e:
        print(f"Error processing DOCX: {str(e)}")

def save_text_with_image_tags(text_content, output_dir, docx_filename):
    text_path = os.path.join(output_dir, f"{docx_filename}_text.txt")
    with open(text_path, "w", encoding="utf-8") as file:
        file.write(text_content)
    print(f"Text extracted and saved to: {text_path}")

def process_docx_files(docx_folder, output_folder):
    create_directory_if_not_exists(docx_folder)
    create_directory_if_not_exists(output_folder)
    
    for filename in os.listdir(docx_folder):
        if filename.lower().endswith('.docx'):
            docx_path = os.path.join(docx_folder, filename)
            print(f"\nProcessing: {filename}")
            process_docx(docx_path, output_folder)

if __name__ == "__main__":
    docx_folder = "./content/source"
    output_folder = "./content/extracted"
    process_docx_files(docx_folder, output_folder) 