"""
Extract text and images from a PPTX file.
"""

import os
import subprocess
from pptx import Presentation
from describe_image import describe_image


def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def convert_slides_to_images(pptx_path, output_dir):
    """Convert PPTX slides to images using LibreOffice."""
    try:
        cmd = [
            'soffice',
            '--headless',
            '--convert-to',
            'png',
            '--outdir',
            output_dir,
            pptx_path
        ]
        subprocess.run(cmd, check=True)
        return sorted([
            f for f in os.listdir(output_dir) 
            if f.endswith('.png')
        ])
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to convert slides: {str(e)}")
    except Exception as e:
        raise Exception(f"Error during slide conversion: {str(e)}")


def process_pptx(pptx_path, output_dir):
    """Process a PPTX file and generate markdown with slide descriptions."""
    try:
        # Create output directory
        create_directory_if_not_exists(output_dir)
        
        # Get presentation filename
        pptx_filename = os.path.splitext(os.path.basename(pptx_path))[0]
        
        # Create temporary directory for slide images
        slides_dir = os.path.join(output_dir, f"{pptx_filename}_slides")
        create_directory_if_not_exists(slides_dir)
        
        # Convert slides to images
        image_files = convert_slides_to_images(pptx_path, slides_dir)
        
        # Generate markdown content
        md_content = f"# {pptx_filename}\n\n"
        
        # Process each slide
        for i, image_file in enumerate(image_files, 1):
            image_path = os.path.join(slides_dir, image_file)
            
            # Get image description
            slide_description = describe_image(image_path)
            
            # Add to markdown
            md_content += f"## Slide {i}\n\n"
            md_content += f"[Image {i}]\n"
            md_content += f"Description: {slide_description}\n\n"
            
            # Clean up image file
            os.remove(image_path)
        
        # Save markdown file
        md_file_path = os.path.join(output_dir, f"{pptx_filename}.md")
        with open(md_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(md_content)
        
        # Clean up slides directory
        os.rmdir(slides_dir)
        
        print(f"Markdown file generated: {md_file_path}")

    except Exception as e:
        print(f"Error processing PPTX: {str(e)}")
        raise


def process_pptx_files(pptx_folder, output_folder):
    """Process all PPTX files in the specified folder."""
    create_directory_if_not_exists(pptx_folder)
    create_directory_if_not_exists(output_folder)

    for filename in os.listdir(pptx_folder):
        if filename.lower().endswith(".pptx"):
            pptx_path = os.path.join(pptx_folder, filename)
            print(f"\nProcessing: {filename}")
            process_pptx(pptx_path, output_folder)


if __name__ == "__main__":
    pptx_folder = "./content/source"
    output_folder = "./content/extracted"
    process_pptx_files(pptx_folder, output_folder)
