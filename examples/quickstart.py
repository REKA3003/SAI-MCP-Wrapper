"""Quickstart for basesmcp.

Mark functions with @mcp, then build and inspect an MCP server via the in-memory client.

Run:  python examples/quickstart.py
"""
from __future__ import annotations

import asyncio

from basesmcp import create_server, mcp


@mcp
async def greet(name: str) -> str:
    """Return a friendly greeting."""
    return f"Hello, {name}!"


@mcp(name="add_numbers", tags={"math"})
async def add(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b


async def main() -> None:
    from fastmcp import Client

    server = create_server(name="Demo MCP", instructions="Example basesmcp tools.")
    async with Client(server) as client:
        tools = await client.list_tools()
        print("Registered tools:", sorted(tool.name for tool in tools))
        print("greet ->", (await client.call_tool("greet", {"name": "Ada"})).data)
        print("add_numbers ->", (await client.call_tool("add_numbers", {"a": 2, "b": 3})).data)


if __name__ == "__main__":
    asyncio.run(main())
