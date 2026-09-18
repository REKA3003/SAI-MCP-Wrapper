"""Access the current MCP request's auth context from inside a tool."""
from __future__ import annotations

from typing import Any, Optional


def current_access_token() -> Optional[Any]:
    """Return the FastMCP ``AccessToken`` for the current request, if any."""
    try:
        from fastmcp.server.dependencies import get_access_token

        return get_access_token()
    except Exception:
        return None


def current_token() -> Optional[str]:
    """Return the raw bearer token string for the current request, if any."""
    access = current_access_token()
    return getattr(access, "token", None) if access is not None else None


def current_claims() -> dict:
    """Return the JWT claims for the current request, if present."""
    access = current_access_token()
    claims = getattr(access, "claims", None) if access is not None else None
    return dict(claims) if claims else {}
