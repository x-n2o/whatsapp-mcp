"""Side-effect-free helpers for MCP server configuration env vars."""

# Accepted WHATSAPP_MCP_TRANSPORT values mapped to FastMCP transport names.
# "http" is a friendly alias for the spec's current "streamable-http" transport.
TRANSPORT_ALIASES = {
    "stdio": "stdio",
    "http": "streamable-http",
    "streamable-http": "streamable-http",
    "streamable_http": "streamable-http",
    "sse": "sse",
}


def resolve_transport(value: str | None) -> str:
    """Map a WHATSAPP_MCP_TRANSPORT value to a FastMCP transport name.

    Raises ValueError for unrecognized values.
    """
    normalized = (value or "stdio").strip().lower()
    try:
        return TRANSPORT_ALIASES[normalized]
    except KeyError:
        accepted = ", ".join(sorted(TRANSPORT_ALIASES))
        raise ValueError(
            f"Invalid WHATSAPP_MCP_TRANSPORT={value!r}; recommended values: stdio, http, sse "
            f"(http maps to the spec's streamable-http transport; all accepted inputs: {accepted})"
        ) from None


def resolve_port(value: str | None) -> int:
    """Parse WHATSAPP_MCP_PORT, falling back to FastMCP's default of 8000.

    Raises ValueError for non-integer or out-of-range values.
    """
    if not value:
        return 8000
    try:
        port = int(value)
    except ValueError:
        raise ValueError(f"Invalid WHATSAPP_MCP_PORT={value!r}; must be an integer") from None
    if not 1 <= port <= 65535:
        raise ValueError(f"Invalid WHATSAPP_MCP_PORT={value!r}; must be between 1 and 65535") from None
    return port
