import pytest
from fastmcp import Client

from basesmcp import ToolRegistry, create_server


@pytest.mark.asyncio
async def test_create_server_registers_and_calls_tools():
    reg = ToolRegistry()

    @reg.register
    async def greet(name: str) -> str:
        """Greet someone by name."""
        return f"Hi {name}"

    server = create_server(name="Test MCP", registry=reg)
    async with Client(server) as client:
        tool_names = {tool.name for tool in await client.list_tools()}
        assert "greet" in tool_names

        result = await client.call_tool("greet", {"name": "Ada"})
        payload = result.data if result.data is not None else result.content[0].text
        assert "Hi Ada" in str(payload)
