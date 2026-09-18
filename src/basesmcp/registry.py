"""Tool registry and the ``@mcp`` marker decorator."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable

logger = logging.getLogger(__name__)


@dataclass
class ToolSpec:
    """A function marked as a tool plus the options to register it with."""

    fn: Callable[..., Any]
    options: dict[str, Any] = field(default_factory=dict)


class ToolRegistry:
    """Collects decorated functions and applies them to a FastMCP server."""

    def __init__(self) -> None:
        self._specs: list[ToolSpec] = []

    def register(self, _fn: Callable[..., Any] | None = None, **options: Any):
        """Mark a function as an MCP tool.

        Usable bare (``@mcp``) or parameterized (``@mcp(name="x", tags={"y"})``). The
        function is returned unchanged so it stays callable and introspectable (FastMCP
        derives the tool schema from its signature and docstring).

        :param _fn: The function when used as a bare decorator; ``None`` with options.
        :param options: Keyword options forwarded to ``FastMCP.tool`` (e.g. ``name``, ``tags``).
        :return: The original function (bare form) or a decorator (parameterized form).
        """

        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            self._specs.append(ToolSpec(fn=fn, options=dict(options)))
            return fn

        if _fn is not None:
            return decorator(_fn)
        return decorator

    @property
    def specs(self) -> list[ToolSpec]:
        """Return a copy of the collected tool specs."""
        return list(self._specs)

    def apply(self, server: Any) -> list[str]:
        """Register every collected tool onto ``server`` and return the tool names."""
        names: list[str] = []
        for spec in self._specs:
            server.tool(**spec.options)(spec.fn)
            names.append(spec.options.get("name", spec.fn.__name__))
        return names

    def clear(self) -> None:
        """Remove all collected specs (useful in tests)."""
        self._specs.clear()


#: Default application-wide registry used by the module-level ``mcp`` decorator.
registry = ToolRegistry()

#: The primary decorator. Import as ``from basesmcp import mcp`` and use ``@mcp``.
mcp = registry.register

#: Readable aliases for the same decorator.
tool = registry.register
mcp_tool = registry.register
