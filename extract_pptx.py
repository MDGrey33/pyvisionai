import os
from pptx import Presentation
from PIL import Image
import io
from describe_image import describe_image

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_text(slide):
    text_content = []
    for shape in slide.shapes:
        if hasattr(shape, "text"):
            text_content.append(shape.text)
    return '\n'.join(text_content)

def extract_images(slide):
    images = []
    for shape in slide.shapes:
        if hasattr(shape, "image"):
            image_data = shape.image.blob
            images.append(image_data)
    return images

def save_image(image_data, output_dir, pptx_filename, slide_index, image_index):
    image = Image.open(io.BytesIO(image_data))
    image_name = f"{pptx_filename}_slide_{slide_index}_image_{image_index}.png"
    img_path = os.path.join(output_dir, image_name)
    image.save(img_path, "PNG")
    return img_path

def process_pptx(pptx_path, output_dir):
    try:
        pptx_filename = os.path.splitext(os.path.basename(pptx_path))[0]
        presentation = Presentation(pptx_path)
        
        text_content = ""
        
        for slide_index, slide in enumerate(presentation.slides):
            slide_text = extract_text(slide)
            image_data_list = extract_images(slide)
            
            for image_index, image_data in enumerate(image_data_list):
                img_path = save_image(image_data, output_dir, pptx_filename, slide_index + 1, image_index + 1)
                image_description = describe_image(img_path)
                image_tag = f"Image: {img_path}\nDescription: {image_description}\n" + "#"*50 + "\n"
                slide_text += "\n" + image_tag
            
            text_content += f"\n--- Slide {slide_index + 1} ---\n" + slide_text
        
        save_text_with_image_tags(text_content, output_dir, pptx_filename)
        
    except Exception as e:
        print(f"Error processing PPTX: {str(e)}")

def save_text_with_image_tags(text_content, output_dir, pptx_filename):
    text_path = os.path.join(output_dir, f"{pptx_filename}_text.txt")
    with open(text_path, "w", encoding="utf-8") as file:
        file.write(text_content)
    print(f"Text extracted and saved to: {text_path}")

if __name__ == "__main__":
    pptx_folder = "./content/source"
    output_folder = "./content/extracted"
    
    create_directory_if_not_exists(pptx_folder)
    create_directory_if_not_exists(output_folder)
    
    for filename in os.listdir(pptx_folder):
        if filename.lower().endswith('.pptx'):
            pptx_path = os.path.join(pptx_folder, filename)
            print(f"\nProcessing: {filename}")
            process_pptx(pptx_path, output_folder) 