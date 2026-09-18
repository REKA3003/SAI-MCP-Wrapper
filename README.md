# basesmcp

Turn any Python function into an auto-registered [MCP](https://modelcontextprotocol.io) tool with a single `@mcp` decorator, then expose them all over a FastMCP server.

## Install

```bash
pip install basesmcp
```

## Quickstart

```python
from basesmcp import mcp, serve

@mcp
def get_user(user_id: str) -> dict:
    """Fetch a user by id."""
    return {"user_id": user_id, "name": "Ada"}

@mcp(name="add_numbers", tags={"math"})
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

if __name__ == "__main__":
    serve(name="My Product MCP", host="0.0.0.0", port=8000, path="/mcp")
```

Any function you decorate with `@mcp` becomes a tool; `serve()` registers them all and runs the server. The MCP client's model selects the right tool per request from its name, description, and type hints — so write clear docstrings and type hints.

## Auto-discovery across modules

Keep tools in a package and let basesmcp import them for you:

```python
from basesmcp import serve

serve(name="My MCP", discover="myproduct.mcp_tools", port=8000)
```

`discover` accepts a module name, a package name (all submodules are imported), or a list of names.

## Auth (optional)

Plug your existing token validation in without basesmcp knowing the details:

```python
from basesmcp import serve, bearer_auth
from fastmcp.server.auth import AccessToken

def verify(token: str):
    claims = my_validate(token)            # your existing logic
    if not claims:
        return None
    return AccessToken(token=token, client_id=claims["sub"], scopes=claims.get("roles", []))

auth = bearer_auth(
    verify=verify,
    authorization_servers=["https://auth.example.com"],
    base_url="https://mcp.example.com",
)
serve(name="My MCP", auth=auth, host="0.0.0.0", port=8000)
```

Read the caller identity inside a tool:

```python
from basesmcp import mcp, current_token, current_claims

@mcp
def whoami() -> dict:
    return {"authenticated": current_token() is not None, "claims": current_claims()}
```

## API

| Symbol | Purpose |
|---|---|
| `@mcp` / `@tool` / `@mcp_tool` | Mark a function as a tool (bare or parameterized). |
| `create_server(name=, instructions=, auth=, discover=, registry=)` | Build a FastMCP server with all tools registered. |
| `serve(..., host=, port=, path=, transport=)` | Build and run the server. |
| `bearer_auth(...)`, `CallbackTokenVerifier` | Optional auth wiring. |
| `current_token()`, `current_claims()`, `current_access_token()` | Current request context. |
| `ToolRegistry` | Isolated registry (e.g. for tests). |

## Best practice

Decorate framework-agnostic functions (plain functions or your service-layer methods) — not web-framework route handlers that depend on request globals. Give every tool a clear docstring and typed parameters so the client model can route to it accurately.

## License

MIT
