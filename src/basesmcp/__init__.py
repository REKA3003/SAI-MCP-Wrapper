"""basesmcp — turn any Python function into an auto-registered MCP tool.

Usage::

    from basesmcp import mcp, serve

    @mcp
    def get_user(user_id: str) -> dict:
        "Fetch a user by id."
        ...

    serve(name="My Product MCP", host="0.0.0.0", port=8000)
"""
from ._context import current_access_token, current_claims, current_token
from .auth import CallbackTokenVerifier, bearer_auth
from .registry import ToolRegistry, ToolSpec, mcp, mcp_tool, registry, tool
from .server import create_server, serve

__version__ = "0.1.0"

__all__ = [
    "mcp",
    "tool",
    "mcp_tool",
    "registry",
    "ToolRegistry",
    "ToolSpec",
    "create_server",
    "serve",
    "bearer_auth",
    "CallbackTokenVerifier",
    "current_access_token",
    "current_token",
    "current_claims",
    "__version__",
]
