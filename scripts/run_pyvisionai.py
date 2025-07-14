#!/usr/bin/env python3
"""
PyVisionAI Server Management Script

Manages both API and MCP servers for PyVisionAI.
"""

import argparse
import subprocess
import sys
import time


def check_docker():
    """Check if Docker is installed and running."""
    try:
        subprocess.run(
            ["docker", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed or not running")
        print("Please install Docker from https://docker.com")
        return False


def is_port_in_use(port):
    """Check if a port is in use."""
    try:
        result = subprocess.run(
            ["lsof", "-i", f":{port}"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        # lsof not available, try netstat
        try:
            result = subprocess.run(
                ["netstat", "-an"],
                capture_output=True,
                text=True,
            )
            return f":{port}" in result.stdout
        except FileNotFoundError:
            # Neither command available, assume port is free
            return False


def get_container_status(container_name):
    """Get the status of a Docker container."""
    try:
        result = subprocess.run(
            [
                "docker",
                "ps",
                "-a",
                "--filter",
                f"name={container_name}",
                "--format",
                "{{.Status}}",
            ],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def start_api_server(build=False):
    """Start the API server."""
    print("\n🚀 Starting API Server...")

    # Check if already running
    if is_port_in_use(8001):
        print("✅ API Server already running on port 8001")
        return True

    try:
        # Build if requested
        if build:
            print("🔨 Building API server...")
            subprocess.run(
                ["docker", "compose", "build"],
                check=True,
            )

        # Start the server
        subprocess.run(
            ["docker", "compose", "up", "-d"],
            check=True,
        )

        # Wait for it to be ready
        print("⏳ Waiting for API server to start...")
        time.sleep(3)

        if is_port_in_use(8001):
            print("✅ API Server started successfully on port 8001")
            print("   📚 Swagger UI: http://localhost:8001/docs")
            return True
        else:
            print("❌ API Server failed to start")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start API server: {e}")
        return False


def start_mcp_server(build=False):
    """Start the MCP server."""
    print("\n🚀 Starting MCP Server...")

    # Check if already running
    if is_port_in_use(8002):
        print("✅ MCP Server already running on port 8002")
        return True

    try:
        # Build if requested
        if build:
            print("🔨 Building MCP server...")
            subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    "docker-compose.mcp.yml",
                    "build",
                ],
                check=True,
            )

        # Start the server
        subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                "docker-compose.mcp.yml",
                "up",
                "-d",
            ],
            check=True,
        )

        # Wait for it to be ready
        print("⏳ Waiting for MCP server to start...")
        time.sleep(3)

        if is_port_in_use(8002):
            print("✅ MCP Server started successfully on port 8002")
            print("   🔗 SSE Endpoint: http://localhost:8002/sse")
            return True
        else:
            print("❌ MCP Server failed to start")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start MCP server: {e}")
        return False


def stop_servers():
    """Stop both servers."""
    print("\n🛑 Stopping servers...")

    try:
        # Stop API server
        subprocess.run(
            ["docker", "compose", "down"],
            capture_output=True,
        )
        print("✅ API Server stopped")
    except Exception:
        pass

    try:
        # Stop MCP server
        subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                "docker-compose.mcp.yml",
                "down",
            ],
            capture_output=True,
        )
        print("✅ MCP Server stopped")
    except Exception:
        pass


def show_status():
    """Show the status of both servers."""
    print("\n📊 PyVisionAI Server Status")
    print("=" * 40)

    # Check API server
    if is_port_in_use(8001):
        print("✅ API Server: Running on port 8001")
        print("   http://localhost:8001/docs")
    else:
        print("❌ API Server: Not running")

    # Check MCP server
    if is_port_in_use(8002):
        print("✅ MCP Server: Running on port 8002")
        print("   http://localhost:8002/sse")
    else:
        print("❌ MCP Server: Not running")

    # Show MCP configuration
    print("\n📝 MCP Configuration for Claude/Cursor:")
    print(
        '   {"mcpServers": {"pyvisionai": {"url": "http://localhost:8002/sse"}}}'
    )
    print("=" * 40)


def main():
    parser = argparse.ArgumentParser(
        description="Manage PyVisionAI servers (API and MCP)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              # Start both servers
  %(prog)s --api        # Start only API server
  %(prog)s --mcp        # Start only MCP server
  %(prog)s --status     # Show server status
  %(prog)s --stop       # Stop all servers
  %(prog)s --build      # Build and start servers
        """,
    )

    parser.add_argument(
        "--api",
        action="store_true",
        help="Start only the API server (port 8001)",
    )
    parser.add_argument(
        "--mcp",
        action="store_true",
        help="Start only the MCP server (port 8002)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show server status",
    )
    parser.add_argument(
        "--stop",
        action="store_true",
        help="Stop all servers",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build Docker images before starting",
    )

    args = parser.parse_args()

    # Check Docker first
    if not check_docker():
        sys.exit(1)

    # Handle commands
    if args.status:
        show_status()
    elif args.stop:
        stop_servers()
    elif args.api:
        if not start_api_server(args.build):
            sys.exit(1)
    elif args.mcp:
        if not start_mcp_server(args.build):
            sys.exit(1)
    else:
        # Default: start both servers
        api_ok = start_api_server(args.build)
        mcp_ok = start_mcp_server(args.build)

        if api_ok and mcp_ok:
            print("\n✨ All servers started successfully!")
            show_status()
        else:
            print("\n⚠️  Some servers failed to start")
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
