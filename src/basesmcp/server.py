"""Build and run a FastMCP server from decorated tools."""
from __future__ import annotations

import importlib
import logging
import pkgutil
from typing import Any, Iterable, Optional, Union

from fastmcp import FastMCP

from .registry import ToolRegistry
from .registry import registry as default_registry

logger = logging.getLogger(__name__)

Discoverable = Union[str, Iterable[str], None]


def _import_targets(discover: Discoverable) -> None:
    """Import modules/packages so their ``@mcp`` decorators run and populate the registry."""
    if not discover:
        return
    targets = [discover] if isinstance(discover, str) else list(discover)
    for target in targets:
        module = importlib.import_module(target)
        if hasattr(module, "__path__"):
            for info in pkgutil.walk_packages(module.__path__, prefix=f"{module.__name__}."):
                importlib.import_module(info.name)


def create_server(
    *,
    name: str = "MCP Server",
    instructions: Optional[str] = None,
    auth: Any = None,
    registry: Optional[ToolRegistry] = None,
    discover: Discoverable = None,
) -> FastMCP:
    """Create a FastMCP server and auto-register every decorated tool.

    :param name: Server name advertised to MCP clients.
    :param instructions: Optional guidance shown to the client model.
    :param auth: Optional FastMCP auth provider (see :func:`basesmcp.bearer_auth`).
    :param registry: Registry to pull tools from (defaults to the module-level registry).
    :param discover: Module/package name(s) to import so their decorators run.
    :return: A configured ``FastMCP`` instance.
    """
    _import_targets(discover)
    reg = registry if registry is not None else default_registry
    server = FastMCP(name=name, instructions=instructions, auth=auth)
    names = reg.apply(server)
    logger.info("Registered %d MCP tools: %s", len(names), ", ".join(sorted(names)))
    return server


def serve(
    *,
    name: str = "MCP Server",
    instructions: Optional[str] = None,
    auth: Any = None,
    host: str = "127.0.0.1",
    port: int = 8000,
    path: str = "/mcp",
    transport: str = "http",
    registry: Optional[ToolRegistry] = None,
    discover: Discoverable = None,
) -> None:
    """Build the server and run it over the given transport (blocking).

    :param host: Bind address (use ``0.0.0.0`` in containers).
    :param port: Bind port.
    :param path: HTTP path the MCP endpoint is served on.
    :param transport: FastMCP transport (``http`` by default).
    """
    server = create_server(
        name=name, instructions=instructions, auth=auth, registry=registry, discover=discover
    )
    server.run(transport=transport, host=host, port=port, path=path)
