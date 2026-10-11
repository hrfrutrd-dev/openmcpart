"""Connect to openmcpart with the official Python MCP client session API."""

import asyncio
import json
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def example_stdio() -> None:
    """Launch the server over stdio, list tools, and call one tool."""
    server_params = StdioServerParameters(command="openmcpart", args=[])
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"Connected. Server exposes {len(tools.tools)} tools.")

            result = await session.call_tool(
                "generate_color_palette",
                {"mood": "calm", "harmony": "analogous", "count": 5},
            )
            for item in result.content:
                if getattr(item, "text", None):
                    print(item.text)


async def example_direct() -> None:
    """Call the in-process MCP server object for a lightweight smoke test."""
    from openmcpart.server import mcp

    result = await mcp.call_tool("check_color_contrast", {"foreground": "#ffffff", "background": "#000000"})
    print("Direct in-process call:")
    print(_result_text(result))


async def example_workflow() -> None:
    """Run a small design-token workflow without an external AI service."""
    from openmcpart.server import mcp

    print("\n=== Design token workflow ===")
    brand = await mcp.call_tool(
        "extract_design_principles",
        {"brand_keywords": "信頼,革新,シンプル", "industry": "SaaS"},
    )
    print("Brand direction:", _result_text(brand)[:400])

    tokens = await mcp.call_tool(
        "generate_design_tokens",
        {"primary_color": "#3b82f6", "brand_name": "MySaaS"},
    )
    try:
        data: Any = json.loads(_result_text(tokens))
        print("CSS variables:")
        print(data["css_variables"])
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"Could not display token output: {exc}")


def _result_text(result: Any) -> str:
    content = getattr(result, "content", [])
    text_parts = [item.text for item in content if getattr(item, "text", None)]
    if text_parts:
        return "\n".join(text_parts)
    return str(result)


async def main() -> None:
    await example_stdio()
    await example_direct()
    await example_workflow()


if __name__ == "__main__":
    asyncio.run(main())
