#!/usr/bin/env python3
"""
Custom prompts example using PyVisionAI.

This script demonstrates how to use custom prompts for different document types
and scenarios, showing how to extract specific types of information.
"""

import os
from typing import Dict

from pyvisionai import create_extractor, describe_image_openai

# Collection of specialized prompts for different use cases
SPECIALIZED_PROMPTS: Dict[str, str] = {
    # Technical documentation prompts
    "technical": (
        "Extract all code snippets, technical terms, and command examples. "
        "For diagrams, describe the technical architecture and components shown."
    ),
    # Business document prompts
    "business": (
        "Extract key business metrics, financial figures, and trends. "
        "For charts, provide detailed analysis of the data presented."
    ),
    # Academic paper prompts
    "academic": (
        "Extract research methodology, key findings, and citations. "
        "For figures, describe the experimental setup and results shown."
    ),
    # Chart analysis prompts
    "chart": (
        "Analyze the chart type, axes labels, and data trends. "
        "Provide key insights and numerical values where visible."
    ),
    # Table extraction prompts
    "table": (
        "Extract table headers and all cell contents precisely. "
        "Maintain the tabular structure in the description."
    ),
}


def example_technical_documentation():
    """Example: Process technical documentation."""
    print("\n=== Technical Documentation Example ===")

    # Create PDF extractor with technical focus
    extractor = create_extractor(
        "pdf", prompt=SPECIALIZED_PROMPTS["technical"]
    )

    try:
        output_path = extractor.extract(
            os.path.join("example_data", "technical_doc.pdf"),
            os.path.join("output", "technical"),
        )
        print(f"Technical content extracted to: {output_path}")
    except FileNotFoundError as e:
        print(
            f"Error processing technical doc: File not found - {e.filename}"
        )
    except PermissionError as e:
        print(
            f"Error processing technical doc: Permission denied - {e.filename}"
        )
    except Exception as e:
        print(
            f"Error processing technical doc: {type(e).__name__}: {str(e)}"
        )


def example_business_report():
    """Example: Process business report with charts."""
    print("\n=== Business Report Example ===")

    # Create PPTX extractor with business focus
    extractor = create_extractor(
        "pptx", prompt=SPECIALIZED_PROMPTS["business"]
    )

    try:
        output_path = extractor.extract(
            os.path.join("example_data", "charts.pptx"),
            os.path.join("output", "business"),
        )
        print(f"Business content extracted to: {output_path}")
    except FileNotFoundError as e:
        print(
            f"Error processing business report: File not found - {e.filename}"
        )
    except PermissionError as e:
        print(
            f"Error processing business report: Permission denied - {e.filename}"
        )
    except Exception as e:
        print(
            f"Error processing business report: {type(e).__name__}: {str(e)}"
        )


def example_research_paper():
    """Example: Process academic research paper."""
    print("\n=== Research Paper Example ===")

    # Create PDF extractor with academic focus
    extractor = create_extractor(
        "pdf", prompt=SPECIALIZED_PROMPTS["academic"]
    )

    try:
        output_path = extractor.extract(
            os.path.join("example_data", "research_paper.pdf"),
            os.path.join("output", "academic"),
        )
        print(f"Academic content extracted to: {output_path}")
    except FileNotFoundError as e:
        print(
            f"Error processing research paper: File not found - {e.filename}"
        )
    except PermissionError as e:
        print(
            f"Error processing research paper: Permission denied - {e.filename}"
        )
    except Exception as e:
        print(
            f"Error processing research paper: {type(e).__name__}: {str(e)}"
        )


def example_chart_analysis():
    """Example: Detailed chart analysis."""
    print("\n=== Chart Analysis Example ===")

    try:
        # Analyze chart using specialized prompt
        description = describe_image_openai(
            os.path.join("example_data", "chart.png"),
            prompt=SPECIALIZED_PROMPTS["chart"],
        )
        print("\nChart Analysis:")
        print(description)
    except FileNotFoundError as e:
        print(f"Error analyzing chart: File not found - {e.filename}")
    except Exception as e:
        print(f"Error analyzing chart: {type(e).__name__}: {str(e)}")


def example_table_extraction():
    """Example: Extract and structure tabular data."""
    print("\n=== Table Extraction Example ===")

    # Create DOCX extractor with table focus
    extractor = create_extractor(
        "docx", prompt=SPECIALIZED_PROMPTS["table"]
    )

    try:
        output_path = extractor.extract(
            os.path.join("example_data", "report.docx"),
            os.path.join("output", "tables"),
        )
        print(f"Table content extracted to: {output_path}")
    except FileNotFoundError as e:
        print(f"Error extracting tables: File not found - {e.filename}")
    except PermissionError as e:
        print(
            f"Error extracting tables: Permission denied - {e.filename}"
        )
    except Exception as e:
        print(f"Error extracting tables: {type(e).__name__}: {str(e)}")


def example_combined_analysis():
    """Example: Combine multiple prompts for complex documents."""
    print("\n=== Combined Analysis Example ===")

    # Create extractor with combined prompts
    combined_prompt = (
        f"For text content: {SPECIALIZED_PROMPTS['technical']}\n"
        f"For charts and graphs: {SPECIALIZED_PROMPTS['chart']}\n"
        f"For tables: {SPECIALIZED_PROMPTS['table']}"
    )

    extractor = create_extractor("pdf", prompt=combined_prompt)

    try:
        output_path = extractor.extract(
            os.path.join("example_data", "complex.pdf"),
            os.path.join("output", "combined"),
        )
        print(f"Combined analysis saved to: {output_path}")
    except FileNotFoundError as e:
        print(
            f"Error in combined analysis: File not found - {e.filename}"
        )
    except PermissionError as e:
        print(
            f"Error in combined analysis: Permission denied - {e.filename}"
        )
    except Exception as e:
        print(
            f"Error in combined analysis: {type(e).__name__}: {str(e)}"
        )


def example_custom_prompt_builder():
    """Example: Build custom prompts based on content type."""
    print("\n=== Custom Prompt Builder Example ===")

    def build_prompt(
        has_charts: bool = False,
        has_tables: bool = False,
        has_code: bool = False,
    ) -> str:
        """Build a custom prompt based on content types."""
        prompt_parts = ["Extract and describe all text content."]

        if has_charts:
            prompt_parts.append(SPECIALIZED_PROMPTS["chart"])
        if has_tables:
            prompt_parts.append(SPECIALIZED_PROMPTS["table"])
        if has_code:
            prompt_parts.append(
                "Extract all code blocks, maintaining proper formatting."
            )

        return " ".join(prompt_parts)

    # Example: Document with charts and tables
    extractor = create_extractor(
        "pdf", prompt=build_prompt(has_charts=True, has_tables=True)
    )

    try:
        output_path = extractor.extract(
            os.path.join("example_data", "mixed_content.pdf"),
            os.path.join("output", "custom"),
        )
        print(f"Custom prompt analysis saved to: {output_path}")
    except FileNotFoundError as e:
        print(
            f"Error in custom analysis: File not found - {e.filename}"
        )
    except PermissionError as e:
        print(
            f"Error in custom analysis: Permission denied - {e.filename}"
        )
    except Exception as e:
        print(f"Error in custom analysis: {type(e).__name__}: {str(e)}")


def main():
    """Run all custom prompt examples."""
    # Create output directories
    for dir_name in [
        "technical",
        "business",
        "academic",
        "tables",
        "combined",
        "custom",
    ]:
        os.makedirs(os.path.join("output", dir_name), exist_ok=True)

    # Run examples
    example_technical_documentation()
    example_business_report()
    example_research_paper()
    example_chart_analysis()
    example_table_extraction()
    example_combined_analysis()
    example_custom_prompt_builder()

    print("\nAll custom prompt examples completed!")


if __name__ == "__main__":
    main()
