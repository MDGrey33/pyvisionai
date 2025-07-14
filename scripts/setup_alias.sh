#!/bin/bash
# Setup alias for PyVisionAI server management

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "Setting up PyVisionAI alias..."

# Detect shell
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo "❌ Unsupported shell: $SHELL"
    echo "Please manually add the following alias to your shell configuration:"
    echo "alias pyvisionai='$PROJECT_DIR/run_servers.sh'"
    exit 1
fi

# Check if alias already exists
if grep -q "alias pyvisionai=" "$SHELL_RC" 2>/dev/null; then
    echo "✅ PyVisionAI alias already exists in $SHELL_RC"
else
    # Add alias
    echo "" >> "$SHELL_RC"
    echo "# PyVisionAI server management" >> "$SHELL_RC"
    echo "alias pyvisionai='$PROJECT_DIR/run_servers.sh'" >> "$SHELL_RC"
    echo "✅ Added PyVisionAI alias to $SHELL_RC"
fi

echo ""
echo "Usage:"
echo "  pyvisionai              # Start both servers"
echo "  pyvisionai --api        # Start only API server"
echo "  pyvisionai --mcp        # Start only MCP server"
echo "  pyvisionai --status     # Check server status"
echo "  pyvisionai --stop       # Stop all servers"
echo ""
echo "To use the alias immediately, run:"
echo "  source $SHELL_RC"
