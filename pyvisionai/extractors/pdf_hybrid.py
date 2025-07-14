"""Hybrid PDF extractor that combines text_and_images and page_as_image methods.

This extractor runs both extraction methods and then uses an LLM to merge
the results into a comprehensive markdown file that has both accurate text
and complete visual context.
"""

import concurrent.futures
import os
import shutil
import tempfile
from datetime import datetime
from typing import Tuple

from pyvisionai.describers import (
    describe_image_ollama,
    describe_image_openai,
)
from pyvisionai.extractors.base import BaseExtractor
from pyvisionai.extractors.pdf import PDFTextImageExtractor
from pyvisionai.extractors.pdf_page import PDFPageImageExtractor
from pyvisionai.utils.config import OPENAI_MODEL_NAME
from pyvisionai.utils.logger import logger


class PDFHybridExtractor(BaseExtractor):
    """Hybrid extractor that combines text_and_images and page_as_image methods."""

    def __init__(self):
        """Initialize the hybrid extractor with both sub-extractors."""
        super().__init__()
        self.text_image_extractor = PDFTextImageExtractor()
        self.page_image_extractor = PDFPageImageExtractor()

    def merge_with_llm(
        self,
        text_md_content: str,
        page_md_content: str,
        pdf_filename: str,
    ) -> str:
        """Use an LLM to intelligently merge the two markdown outputs.

        Args:
            text_md_content: Markdown from text_and_images extraction
            page_md_content: Markdown from page_as_image extraction
            pdf_filename: Name of the PDF file

        Returns:
            Merged markdown content
        """
        merge_prompt = f"""TASK: Copy the text below EXACTLY as written, then add visual styling information.

ORIGINAL TEXT TO COPY (copy every word exactly):
{text_md_content}

VISUAL STYLING ANALYSIS (use to enhance formatting):
{page_md_content}

RULES:
- Copy EVERY SINGLE WORD from ORIGINAL TEXT exactly
- Do NOT change, improve, or rewrite ANY text content
- Keep ALL special characters (○, ●, •) exactly as shown
- Apply markdown formatting (bold, italics) based on VISUAL STYLING ANALYSIS
- Add [Image: description] for visual elements mentioned in STYLING ANALYSIS
- Preserve exact page structure from ORIGINAL TEXT
- Change filename to: {pdf_filename}

START COPYING THE ORIGINAL TEXT WITH VISUAL ENHANCEMENTS:"""

        try:
            if self.model == "llama":
                # For Ollama, we need to save the prompt as a temporary file
                # since it might be too long for command line
                with tempfile.NamedTemporaryFile(
                    mode='w', suffix='.txt', delete=False
                ) as f:
                    f.write(merge_prompt)
                    prompt_file = f.name

                try:
                    # Use Ollama with the prompt file
                    merged_content = describe_image_ollama(
                        prompt_file,  # Ollama will read this as the prompt
                        model="llama3.2:latest",  # Use text model, not vision
                        prompt=merge_prompt,
                    )
                finally:
                    os.unlink(prompt_file)

            else:  # GPT-4
                # For OpenAI, we can use the API directly with the long prompt
                import openai

                client = openai.OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=OPENAI_MODEL_NAME,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert at merging document extractions to create comprehensive markdown documents.",
                        },
                        {"role": "user", "content": merge_prompt},
                    ],
                    max_tokens=4000,
                    temperature=0.3,
                )
                merged_content = response.choices[0].message.content

            return merged_content

        except Exception as e:
            logger.error(f"Error merging with LLM: {str(e)}")
            # Fallback: return the page extraction as it's usually more complete
            logger.warning("Falling back to page_as_image extraction")
            return page_md_content

    def extract(self, pdf_path: str, output_dir: str) -> str:
        """Extract content using both methods and merge the results.

        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save the output

        Returns:
            Path to the merged markdown file
        """
        # Create a unique temporary directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        temp_base = tempfile.gettempdir()
        temp_dir = os.path.join(
            temp_base, f"hybrid_extract_{timestamp}"
        )
        os.makedirs(temp_dir, exist_ok=True)

        try:
            pdf_filename = os.path.splitext(os.path.basename(pdf_path))[
                0
            ]
            logger.info(
                f"Starting hybrid extraction for {pdf_filename}"
            )

            # Run both extractions in parallel for better performance
            logger.info(
                "Running both extraction methods in parallel..."
            )

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=2
            ) as executor:
                # Create separate subdirectories to avoid filename conflicts
                text_dir = os.path.join(temp_dir, "text_extraction")
                page_dir = os.path.join(temp_dir, "page_extraction")
                os.makedirs(text_dir, exist_ok=True)
                os.makedirs(page_dir, exist_ok=True)

                # Configure both extractors
                self.text_image_extractor.model = self.model
                self.text_image_extractor.api_key = self.api_key
                self.text_image_extractor.prompt = self.prompt

                # Configure page extractor with custom prompt for visual analysis only
                visual_prompt = """Analyze this document page for VISUAL and STYLING elements only. Focus on:

1. IMAGES/FIGURES: Describe any images, charts, diagrams, or visual elements
2. LAYOUT: Document structure, columns, spacing, visual hierarchy
3. FORMATTING: Bold text, italics, headers, bullet styles, font variations
4. VISUAL DESIGN: Colors, borders, backgrounds, visual emphasis
5. SPATIAL RELATIONSHIPS: How elements are positioned relative to each other

DO NOT transcribe or describe the text content itself - only focus on the visual presentation, styling, and layout structure. Describe what you see visually, not what the text says."""

                self.page_image_extractor.model = self.model
                self.page_image_extractor.api_key = self.api_key
                self.page_image_extractor.prompt = visual_prompt

                # Submit both extraction tasks to separate directories
                text_future = executor.submit(
                    self.text_image_extractor.extract,
                    pdf_path,
                    text_dir,
                )
                page_future = executor.submit(
                    self.page_image_extractor.extract,
                    pdf_path,
                    page_dir,
                )

                # Wait for both to complete
                text_md_path = text_future.result()
                page_md_path = page_future.result()

            # Read the results
            with open(text_md_path, 'r', encoding='utf-8') as f:
                text_md_content = f.read()

            with open(page_md_path, 'r', encoding='utf-8') as f:
                page_md_content = f.read()

            # Step 3: Merge using LLM
            logger.info("Merging extractions using LLM...")
            merged_content = self.merge_with_llm(
                text_md_content, page_md_content, pdf_filename
            )

            # Step 4: Save the merged result
            output_path = os.path.join(
                output_dir, f"{pdf_filename}_pdf.md"
            )
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(merged_content)

            logger.info(f"Hybrid extraction completed: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error in hybrid extraction: {str(e)}")
            raise
        finally:
            # Clean up temporary directory
            if os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                except Exception as e:
                    logger.warning(
                        f"Failed to cleanup temp directory {temp_dir}: {e}"
                    )
