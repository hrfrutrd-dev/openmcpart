"""
Example client for openmcpart design MCP server
どんなAgentでも使えることを示すクライアント例

This example shows how ANY agent can use this MCP server.
"""

import asyncio
from mcp import Client
from mcp.client.stdio import StdioServerParameters

async def example_stdio():
    """Example using stdio transport (most common)"""
    print("=== stdio transport example ===")
    
    # For Claude Desktop, Cursor, etc., you don't need to write client code
    # Just configure the MCP server in config file.
    # This is for custom agents that want to call the server programmatically.
    
    server_params = StdioServerParameters(
        command="openmcpart",
        args=[],
    )
    
    # This would be used like:
    # async with Client(server_params) as client:
    #     result = await client.call_tool("generate_color_palette", {"mood": "calm"})
    #     print(result)
    
    print("Configure in your MCP client config:")
    print("""
{
  "mcpServers": {
    "openmcpart-design": {
      "command": "openmcpart",
      "args": []
    }
  }
}
    """)

async def example_direct():
    """Direct usage without MCP transport (for testing)"""
    print("\n=== Direct tool usage (no transport) ===")
    
    from openmcpart.server import mcp
    
    # Call tools directly
    tools_to_try = [
        ("generate_color_palette", {"mood": "calm", "harmony": "analogous"}),
        ("check_color_contrast", {"foreground": "#ffffff", "background": "#3b82f6"}),
        ("suggest_typography_pairing", {"mood": "tech_trust", "language": "ja"}),
        ("generate_design_tokens", {"primary_color": "#6366f1", "brand_name": "DemoBrand"}),
    ]
    
    for tool_name, args in tools_to_try:
        print(f"\n--- {tool_name}({args}) ---")
        result = await mcp.call_tool(tool_name, args)
        # result is CallToolResult with content
        if hasattr(result, 'content') and result.content:
            text = result.content[0].text
            # Truncate for display
            print(text[:600] + "..." if len(text) > 600 else text)
        else:
            print(result)

async def example_workflow():
    """Full workflow: branding -> colors -> typography -> tokens -> layout"""
    print("\n=== Full Design Workflow Example ===")
    
    from openmcpart.server import mcp
    
    # 1. Branding
    print("\n1. ブランディング分析...")
    r1 = await mcp.call_tool("extract_design_principles", {
        "brand_keywords": "信頼,革新,シンプル",
        "industry": "SaaS",
        "audience": "スタートアップ"
    })
    print(r1.content[0].text[:500])
    
    # 2. Color
    print("\n2. カラーパレット生成...")
    r2 = await mcp.call_tool("generate_color_palette", {
        "mood": "tech",
        "harmony": "analogous"
    })
    print(r2.content[0].text[:500])
    
    # 3. Typography
    print("\n3. タイポグラフィ...")
    r3 = await mcp.call_tool("suggest_typography_pairing", {
        "mood": "tech_trust",
        "industry": "saas",
        "language": "en"
    })
    print(r3.content[0].text[:500])
    
    # 4. Tokens
    print("\n4. デザイントークン...")
    r4 = await mcp.call_tool("generate_design_tokens", {
        "primary_color": "#3b82f6",
        "brand_name": "MySaaS"
    })
    text = r4.content[0].text
    # Parse JSON to get css_variables
    import json
    data = json.loads(text)
    print("CSS Variables:")
    print(data["css_variables"][:500])
    
    # 5. Layout
    print("\n5. レイアウト提案...")
    r5 = await mcp.call_tool("suggest_layout", {
        "content_type": "landing_saas",
        "target": "desktop",
        "style": "minimal"
    })
    print(r5.content[0].text[:500])

if __name__ == "__main__":
    asyncio.run(example_stdio())
    asyncio.run(example_direct())
    asyncio.run(example_workflow())
