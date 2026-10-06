import pytest
from openmcpart.server import mcp

def test_mcp_instance():
    assert mcp is not None
    assert mcp.name == "openmcpart-design"

# Check tools are registered
def test_tools_registered():
    # FastMCP stores tools internally, we can check via list_tools
    import asyncio
    
    async def get_tools():
        tools = await mcp.list_tools()
        return tools
    
    tools = asyncio.run(get_tools())
    tool_names = [t.name for t in tools]
    
    expected = [
        "generate_color_palette",
        "check_color_contrast",
        "generate_gradient",
        "suggest_typography_pairing",
        "generate_type_scale",
        "suggest_layout",
        "generate_spacing_system",
        "generate_design_tokens",
        "generate_tailwind_config",
        "check_accessibility",
        "critique_design",
        "suggest_component_variants",
        "extract_design_principles",
        "generate_moodboard_brief",
    ]
    
    for name in expected:
        assert name in tool_names, f"Tool {name} not registered. Found: {tool_names}"

def test_resources_registered():
    import asyncio
    
    async def get_resources():
        resources = await mcp.list_resources()
        return resources
    
    resources = asyncio.run(get_resources())
    uris = [str(r.uri) for r in resources]
    assert "design://tokens/template" in uris
    assert "design://guidelines/8pt-grid" in uris
