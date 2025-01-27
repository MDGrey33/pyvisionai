
```mermaid
graph TD
    classDef required fill:#ff6666,stroke:#ff0000,stroke-width:2px,color:black
    classDef optional fill:#98FB98,stroke:#00ff00,stroke-width:2px,color:black
    classDef default fill:#87CEEB,stroke:#4682B4,stroke-width:2px,color:black
    classDef example fill:#FFE4B5,stroke:#FFD700,stroke-width:2px,color:black

    CLI(["describe-image"])

    subgraph EXAMPLES["✨ EXAMPLES"]
        Basic["Quickstart:
        describe-image -i photo.jpg"]

        Local["Local Model:
        describe-image -i photo.jpg -u llama"]
    end

    subgraph OPTIONAL["🟢 OPTIONAL"]
        Model["--use-case, -u
        🤖 Model Choice
        gpt4 | llama"]

        Key["--api-key, -k
        🔑 OpenAI Key"]

        Verbose["--verbose, -v
        📝 Detailed Output"]

        Prompt["--prompt, -p
        💭 Custom Instructions"]
    end

    subgraph REQUIRED["🔴 REQUIRED"]
        Image["--image, -i
        📸 Image File Path"]
    end

    subgraph DEFAULTS["🔵 DEFAULTS"]
        ModelDefault["🤖 gpt4"]
        KeyDefault["🔑 From ENV (OPENAI_API_KEY)"]
        VerboseDefault["📝 Off"]
        PromptDefault["💭 Describe this image in detail"]
    end

    CLI --> Image
    CLI --> Model & Key & Verbose & Prompt

    Model --> ModelDefault
    Key --> KeyDefault
    Verbose --> VerboseDefault
    Prompt --> PromptDefault

    class Image required
    class Model,Key,Verbose,Prompt optional
    class ModelDefault,KeyDefault,VerboseDefault,PromptDefault default
    class Basic,Local example
