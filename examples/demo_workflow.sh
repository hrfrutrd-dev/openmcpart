#!/bin/bash
# Demo workflow showing universal agent compatibility

echo "=== openmcpart Design MCP Server Demo ==="
echo ""

echo "1. Testing direct tool calls..."
python3 -c "
import asyncio
from openmcpart.server import mcp

async def demo():
    print('🎨 カラーパレット生成 (mood: calm)')
    r = await mcp.call_tool('generate_color_palette', {'mood': 'calm'})
    import json
    data = json.loads(r.content[0].text)
    print(f\"Primary: {data['primary']}\")
    print(f\"Secondary: {data['secondary']}\")
    print(f\"CSS: {data['css_variables'][:100]}...\")
    
    print('\n♿ コントラストチェック')
    r = await mcp.call_tool('check_color_contrast', {'foreground': '#ffffff', 'background': '#3b82f6'})
    data = json.loads(r.content[0].text)
    print(f\"Ratio: {data['ratio']} - {data['recommendation']}\")
    
    print('\n✍️ タイポグラフィ提案')
    r = await mcp.call_tool('suggest_typography_pairing', {'mood': 'modern_minimal', 'language': 'ja'})
    data = json.loads(r.content[0].text)
    print(f\"Heading: {data['pairing']['heading']}\")
    print(f\"Body: {data['pairing']['body']}\")

asyncio.run(demo())
"

echo ""
echo "2. MCP Inspector でテストする場合:"
echo "   npx @modelcontextprotocol/inspector openmcpart"
echo ""
echo "3. Claude Desktop設定:"
echo "   cat examples/claude_desktop_config.json"
echo ""
echo "✅ Demo complete! このMCPサーバーはどんなAgentでも使えます"
