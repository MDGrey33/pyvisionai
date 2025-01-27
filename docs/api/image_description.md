```mermaid
graph TD
    classDef function fill:#4169E1,stroke:#000080,stroke-width:2px,color:white
    classDef required fill:#ff6666,stroke:#ff0000,stroke-width:2px,color:black
    classDef optional fill:#98FB98,stroke:#00ff00,stroke-width:2px,color:black
    classDef default fill:#87CEEB,stroke:#4682B4,stroke-width:2px,color:black
    classDef example fill:#FFE4B5,stroke:#FFD700,stroke-width:2px,color:black

    subgraph IMPORTS["📦 IMPORTS"]
        Import["from pyvisionai import
        describe_image_openai,
        describe_image_ollama"]
    end

    subgraph FUNCTIONS["🔵 FUNCTIONS"]
        OpenAI["describe_image_openai()"]
        Ollama["describe_image_ollama()"]
    end

    subgraph EXAMPLES["✨ EXAMPLES"]
        OpenAIExample["description = describe_image_openai('image.jpg', model='gpt4', api_key='key', prompt='custom prompt')"]

        OllamaExample["description = describe_image_ollama('image.jpg', model='llama3.2-vision', prompt='custom prompt')"]
    end

    subgraph OPENAI_PARAMS["📝 OpenAI Parameters"]
        OpenAIRequired["🔴 Required:
        image_path: str"]

        OpenAIOptional["🟢 Optional:
        model: str = 'gpt-4-vision-preview'
        api_key: str = None (from env)
        prompt: str = DEFAULT_PROMPT
        max_tokens: int = 300"]
    end

    subgraph OLLAMA_PARAMS["📝 Ollama Parameters"]
        OllamaRequired["🔴 Required:
        image_path: str"]

        OllamaOptional["🟢 Optional:
        model: str = 'llama3.2-vision'
        prompt: str = DEFAULT_PROMPT"]
    end

    Import --> OpenAI & Ollama
    OpenAI --> OpenAIRequired & OpenAIOptional --> OpenAIExample
    Ollama --> OllamaRequired & OllamaOptional --> OllamaExample

    class OpenAI,Ollama function
    class OpenAIRequired,OllamaRequired required
    class OpenAIOptional,OllamaOptional optional
    class OpenAIExample,OllamaExample example
