"""
openmcpart - Universal Design Specialist MCP Server
どんなAgentでも使えるデザイン専門MCPサーバー
"""

__version__ = "0.2.0"
__description__ = "Universal Design Specialist MCP Server - any agent can use"

from .server import mcp, main

__all__ = ["mcp", "main"]
