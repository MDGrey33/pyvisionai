```mermaid
graph TD
    classDef required fill:#ff6666,stroke:#ff0000,stroke-width:2px,color:black
    classDef optional fill:#98FB98,stroke:#00ff00,stroke-width:2px,color:black
    classDef default fill:#87CEEB,stroke:#4682B4,stroke-width:2px,color:black
    classDef example fill:#FFE4B5,stroke:#FFD700,stroke-width:2px,color:black

    CLI(["file-extract"])

    subgraph EXAMPLES["✨ EXAMPLES"]
        Basic["Quickstart:
        file-extract -t pdf -s document.pdf -o ./output"]

        Directory["Directory:
        file-extract -t pdf -s ./docs -o ./output"]

        Advanced["Advanced:
        file-extract -t pdf -s document.pdf -o ./output -e text_and_images -m llama"]
    end

    subgraph OPTIONAL["🟢 OPTIONAL"]
        Extractor["--extractor, -e
        📄 Extraction Method
        text_and_images | page_as_image"]

        Model["--model, -m
        🤖 Model Choice
        llama | gpt4"]

        Key["--api-key, -k
        🔑 OpenAI Key"]

        Prompt["--prompt, -p
        💭 Custom Instructions"]
    end

    subgraph REQUIRED["🔴 REQUIRED"]
        Type["--type, -t
        📄 File Type
        pdf | docx | pptx | html"]

        Source["--source, -s
        📥 Source Path
        (file or directory)"]

        Output["--output, -o
        📤 Output Directory"]
    end

    subgraph DEFAULTS["🔵 DEFAULTS"]
        ExtractorDefault["📄 page_as_image"]
        ModelDefault["🤖 gpt4"]
        KeyDefault["🔑 From ENV (OPENAI_API_KEY)"]
        PromptDefault["💭 Describe this image in detail.
        Preserve as much of the precise original
        text, format, images and style as possible."]
        SourceDefault["📥 content/source"]
        OutputDefault["📤 content/extracted"]
    end

    CLI --> Type & Source & Output
    CLI --> Extractor & Model & Key & Prompt

    Extractor --> ExtractorDefault
    Model --> ModelDefault
    Key --> KeyDefault
    Prompt --> PromptDefault
    Source --> SourceDefault
    Output --> OutputDefault

    class Type,Source,Output required
    class Extractor,Model,Key,Prompt optional
    class ExtractorDefault,ModelDefault,KeyDefault,PromptDefault,SourceDefault,OutputDefault default
    class Basic,Directory,Advanced example
```

## Default Prompt

The tool uses a single default prompt for all extraction methods and models:

```
"Describe this image in detail. Preserve as much of the precise original text, format, images and style as possible."
```

This prompt is designed to:
1. Extract text content accurately
2. Maintain original formatting
3. Describe visual elements
4. Preserve document structure

## Custom Prompt Guidelines

When using custom prompts, ensure they include:

1. **For Both Methods**
   - Clear instruction to describe visual content
   - Request for maintaining precision and detail

2. **For page_as_image Method**
   - Additional instruction to extract and preserve text content
   - Example: "Extract all text exactly as shown and describe any visual elements in detail"

3. **For text_and_images Method**
   - Focus on visual description (text is handled separately)
   - Example: "Describe all visual elements, diagrams, and their relationships"

## Specialized Prompts by Use Case

| Use Case | Extraction Method | Recommended Prompt |
|----------|------------------|-------------------|
| Technical Documentation | page_as_image | "Extract all code snippets, technical terms, and command examples. For diagrams, describe the technical architecture and components shown." |
| Business Documents | page_as_image | "Extract key business metrics, financial figures, and trends. For charts, provide detailed analysis of the data presented." |
| Academic Papers | page_as_image | "Extract research methodology, key findings, and citations. For figures, describe the experimental setup and results shown." |
| Charts & Diagrams | text_and_images | "Analyze the chart type, axes labels, and data trends. Provide key insights and numerical values where visible." |
| Tables | text_and_images | "Extract table headers and all cell contents precisely. Maintain the tabular structure in the description." |
