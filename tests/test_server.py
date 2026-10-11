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
        "generate_sophisticated_ui",
        "critique_ai_look",
        "audit_project",
        "extract_project_tokens",
    ]

    assert len(tool_names) == len(expected)
    for name in expected:
        assert name in tool_names, f"Tool {name} not registered. Found: {tool_names}"

def test_http_transport_defaults_to_loopback(monkeypatch, capsys):
    import openmcpart.server as server

    monkeypatch.delenv("MCP_HOST", raising=False)
    calls = []
    monkeypatch.setattr(server.mcp, "run", lambda **kwargs: calls.append(kwargs))

    assert server.main(["--transport", "streamable-http"]) == 0
    assert calls[0]["host"] == "127.0.0.1"
    assert calls[0]["port"] == 8000
    capsys.readouterr()


def test_project_audit_tools_require_an_explicit_path():
    import asyncio

    async def get_tools():
        return await mcp.list_tools()

    tool_schemas = {tool.name: tool.input_schema for tool in asyncio.run(get_tools())}
    for name in ("audit_project", "extract_project_tokens"):
        assert "project_path" in tool_schemas[name].get("required", [])
        assert "default" not in tool_schemas[name]["properties"]["project_path"]


def test_resources_registered():
    import asyncio
    
    async def get_resources():
        resources = await mcp.list_resources()
        return resources
    
    resources = asyncio.run(get_resources())
    uris = [str(r.uri) for r in resources]
    assert set(uris) == {
        "design://tokens/template",
        "design://guidelines/8pt-grid",
        "design://guidelines/wcag",
        "design://checklist/design-review",
    }


def test_prompts_registered():
    import asyncio

    async def get_prompts():
        return await mcp.list_prompts()

    prompts = asyncio.run(get_prompts())
    assert {prompt.name for prompt in prompts} == {
        "design_critique_prompt",
        "branding_workshop_prompt",
        "component_design_prompt",
    }
