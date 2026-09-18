"""Optional helpers for plugging product-specific bearer-token auth into the server."""
from __future__ import annotations

import inspect
from typing import Any, Callable, Iterable

try:
    from fastmcp.server.auth import RemoteAuthProvider, TokenVerifier
    from pydantic import AnyHttpUrl

    _AUTH_AVAILABLE = True
except Exception:  # pragma: no cover - depends on optional fastmcp auth surface
    RemoteAuthProvider = Any  # type: ignore[assignment,misc]
    TokenVerifier = object  # type: ignore[assignment,misc]
    AnyHttpUrl = str  # type: ignore[assignment,misc]
    _AUTH_AVAILABLE = False

VerifyCallback = Callable[[str], Any]


class CallbackTokenVerifier(TokenVerifier):
    """Adapt a product-supplied ``verify(token)`` callable to a FastMCP token verifier.

    The callback receives the raw bearer token and returns a FastMCP ``AccessToken`` on
    success or ``None`` on failure. It may be synchronous or asynchronous.
    """

    def __init__(self, verify: VerifyCallback) -> None:
        super().__init__()
        self._verify = verify

    async def verify_token(self, token: str):  # type: ignore[override]
        result = self._verify(token)
        if inspect.isawaitable(result):
            result = await result
        return result


def bearer_auth(
    *,
    verify: VerifyCallback,
    authorization_servers: Iterable[str],
    base_url: str,
):
    """Build a FastMCP ``RemoteAuthProvider`` from a custom token-verify callback.

    :param verify: Callable returning a FastMCP ``AccessToken`` or ``None``.
    :param authorization_servers: Authorization-server URLs advertised in OAuth metadata.
    :param base_url: Public base URL of this MCP server.
    :raises RuntimeError: If the installed FastMCP does not expose the auth surface.
    """
    if not _AUTH_AVAILABLE:
        raise RuntimeError("FastMCP auth surface is unavailable in this environment.")
    return RemoteAuthProvider(
        token_verifier=CallbackTokenVerifier(verify),
        authorization_servers=[AnyHttpUrl(url) for url in authorization_servers],
        base_url=base_url,
    )
