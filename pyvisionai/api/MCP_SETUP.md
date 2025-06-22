# PyVisionAI MCP Server Setup Guide

This guide explains how to use PyVisionAI as an MCP (Model Context Protocol) server, allowing AI agents like Claude Desktop to discover and use your image description tools.

## What is MCP?

[MCP (Model Context Protocol)](https://medium.com/@ruchi.awasthi63/integrating-mcp-servers-with-fastapi-2c6d0c9a4749) is a standardized communication layer that enables AI agents to understand and interact with external APIs. It provides a structured way for APIs to describe their capabilities, input schemas, and execution methods.

## Starting the MCP Server

### 1. Start the FastAPI server with MCP support:

```bash
cd /path/to/file_extractor
poetry run uvicorn pyvisionai.api.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Verify MCP endpoint is available:

Visit http://127.0.0.1:8000/mcp in your browser. You should see the MCP server information.

## Configuring Claude Desktop to Use PyVisionAI

### 1. Locate Claude Desktop Configuration

Find your `claude_desktop_config.json` file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 2. Add PyVisionAI MCP Configuration

Edit the configuration file and add your PyVisionAI server:

```json
{
  "mcpServers": {
    "pyvisionai": {
      "command": "mcp-proxy",
      "args": ["http://127.0.0.1:8000/mcp"],
      "description": "PyVisionAI image description service with OpenAI, Claude, and Ollama support",
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key",
        "ANTHROPIC_API_KEY": "your-anthropic-api-key"
      }
    }
  }
}
```

**Alternative setup using virtual environment:**

If you installed mcp-proxy in your project's virtual environment:

```json
{
  "mcpServers": {
    "pyvisionai": {
      "command": "/path/to/file_extractor/.venv/bin/mcp-proxy",
      "args": ["http://127.0.0.1:8000/mcp"],
      "cwd": "/path/to/file_extractor",
      "description": "PyVisionAI image description service",
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key",
        "ANTHROPIC_API_KEY": "your-anthropic-api-key"
      }
    }
  }
}
```

### 3. Restart Claude Desktop

Close and reopen Claude Desktop. You should see PyVisionAI listed in:
**Claude Settings > Developer > MCP Servers**

## Available Tools in Claude

Once connected, Claude will have access to these image description tools:

1. **describe_image_with_openai** - Analyze images using OpenAI's GPT-4 Vision
2. **describe_image_with_ollama** - Use local Ollama models for private image analysis
3. **describe_image_with_claude** - Analyze images with Anthropic's Claude Vision
4. **describe_image_auto** - Let the system choose the best available model

## Using PyVisionAI Tools in Claude

You can now ask Claude to analyze images using natural language:

- "Use OpenAI to describe this image: [upload image]"
- "Analyze this photo using the local Ollama model"
- "What's in this picture? Use Claude Vision"
- "Describe this image (use any available model)"

Claude will automatically:
1. Recognize your request involves image analysis
2. Select the appropriate PyVisionAI tool
3. Process your image through the MCP server
4. Return the AI-generated description

## Docker Deployment (Optional)

For production use, you can run PyVisionAI in a Docker container:

### 1. Create a Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY pyvisionai ./pyvisionai

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Expose port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "pyvisionai.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Build and run:

```bash
docker build -t pyvisionai-mcp .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e ANTHROPIC_API_KEY=your-key \
  pyvisionai-mcp
```

### 3. Update Claude configuration for Docker:

```json
{
  "mcpServers": {
    "pyvisionai-docker": {
      "command": "mcp-proxy",
      "args": ["http://localhost:8000/mcp"],
      "description": "PyVisionAI MCP server running in Docker"
    }
  }
}
```

## Troubleshooting

### MCP Server Not Showing in Claude

1. Ensure the FastAPI server is running
2. Check that mcp-proxy is installed: `poetry show mcp-proxy`
3. Verify the configuration file syntax is correct (valid JSON)
4. Check Claude's developer console for error messages

### Connection Errors

1. Verify the server URL is correct: http://127.0.0.1:8000/mcp
2. Ensure no firewall is blocking the connection
3. Check the server logs for any errors

### API Key Issues

1. Set environment variables before starting the server:
   ```bash
   export OPENAI_API_KEY="your-key"
   export ANTHROPIC_API_KEY="your-key"
   poetry run uvicorn pyvisionai.api.main:app --reload
   ```

2. Or include them in the Claude configuration as shown above

## Advanced Configuration

### Custom MCP Route

The MCP server is mounted at the root by default. To mount at a custom path:

```python
# In pyvisionai/api/main.py
mcp.mount(path="/custom-mcp-path")
```

Then update your Claude configuration:
```json
"args": ["http://127.0.0.1:8000/custom-mcp-path"]
```

### Multiple Model Configurations

You can set up multiple configurations for different use cases:

```json
{
  "mcpServers": {
    "pyvisionai-openai": {
      "command": "mcp-proxy",
      "args": ["http://127.0.0.1:8000/mcp"],
      "description": "PyVisionAI with OpenAI only",
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    },
    "pyvisionai-local": {
      "command": "mcp-proxy",
      "args": ["http://127.0.0.1:8001/mcp"],
      "description": "PyVisionAI with local Ollama only"
    }
  }
}
```

## Further Reading

- [MCP Documentation](https://modelcontextprotocol.io/introduction)
- [FastAPI-MCP on GitHub](https://github.com/modelcontextprotocol/fastapi-mcp)
- [Integrating MCP Servers with FastAPI](https://medium.com/@ruchi.awasthi63/integrating-mcp-servers-with-fastapi-2c6d0c9a4749)
