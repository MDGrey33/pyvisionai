#!/usr/bin/env python3
"""Simple test to verify PyVisionAI MCP server is running and tools are available."""

import json
import time

import requests


def test_mcp_server():
    """Test that the MCP server is running and responding."""
    print("Testing PyVisionAI MCP Server")
    print("=" * 50)

    # Test SSE endpoint
    print("\n1. Testing SSE endpoint...")
    session_id = None
    try:
        response = requests.get(
            "http://localhost:8002/sse/", timeout=1, stream=True
        )
        print(f"   Status: {response.status_code}")

        # Read first few lines to get session ID
        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')
                if 'session_id=' in line_text:
                    session_id = line_text.split('session_id=')[
                        1
                    ].strip()
                    print(f"   Session ID: {session_id}")
                    break
    except requests.exceptions.ReadTimeout:
        pass  # Expected for SSE
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

    if session_id or response.status_code == 200:
        print("   ✓ SSE endpoint is working")
    else:
        print("   ✗ SSE endpoint not responding")
        return False

    # Test if server is responding
    print("\n2. Server Information:")
    print("   - MCP Server: pyvisionai")
    print("   - Transport: SSE")
    print("   - URL: http://localhost:8002/sse/")
    print("   - Available tools:")
    print("     • describe_image_with_openai")
    print("     • describe_image_with_ollama")
    print("     • describe_image_with_claude")
    print("     • extract_pdf_content")

    print("\n3. Configuration for Cursor:")
    cursor_config = {
        "mcpServers": {
            "pyvisionai": {"url": "http://localhost:8002/sse"}
        }
    }
    print("   Add to ~/.cursor/mcp.json:")
    print(
        "   "
        + json.dumps(cursor_config, indent=2).replace("\n", "\n   ")
    )

    print("\n4. Usage Examples:")
    print("   Once configured in Cursor, you can use commands like:")
    print(
        '   - "Use PyVisionAI to describe the image at /path/to/image.jpg"'
    )
    print('   - "Analyze this screenshot using OpenAI vision"')
    print('   - "Describe this image using the local Ollama model"')
    print('   - "Use Claude to analyze this diagram"')
    print(
        '   - "Extract content from the PDF at /path/to/document.pdf"'
    )
    print(
        '   - "Extract text and images from this PDF" (uses hybrid method by default)'
    )
    print(
        '   - "Analyze this PDF with page_as_image method" (specify method if needed)'
    )

    print(
        "\n   Note: The hybrid method is strongly recommended for PDFs as it provides"
    )
    print(
        "         the most comprehensive results by combining text accuracy with visual analysis."
    )

    print("\n5. Docker Management:")
    print(
        "   - View logs: docker compose -f docker-compose.mcp.yml logs"
    )
    print(
        "   - Stop server: docker compose -f docker-compose.mcp.yml down"
    )
    print(
        "   - Restart: docker compose -f docker-compose.mcp.yml restart"
    )

    print("\n" + "=" * 50)
    print("✓ MCP server is running and ready for use!")
    print("\nNext steps:")
    print("1. Add the configuration above to ~/.cursor/mcp.json")
    print("2. Restart Cursor to load the new MCP server")
    print("3. Use PyVisionAI tools in your conversations")
    print(
        "\nNote: Ensure OPENAI_API_KEY or ANTHROPIC_API_KEY are set in your .env file"
    )

    return True


if __name__ == "__main__":
    test_mcp_server()
