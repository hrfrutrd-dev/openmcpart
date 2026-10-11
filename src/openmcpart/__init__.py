"""
openmcpart - design tools and local audit MCP server
MCP対応クライアント向けのデザイン支援・ローカル監査ツール
"""

__version__ = "0.3.0"
__description__ = "Design tools and read-only local project audit over MCP"

from .server import mcp, main

__all__ = ["mcp", "main"]
