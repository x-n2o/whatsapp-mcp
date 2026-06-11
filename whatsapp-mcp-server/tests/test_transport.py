"""Tests for MCP transport selection."""

import pytest

from mcp_config import resolve_port, resolve_transport


class TestResolveTransport:
    """Tests for resolve_transport()."""

    def test_default_is_stdio(self):
        assert resolve_transport(None) == "stdio"
        assert resolve_transport("") == "stdio"

    def test_http_alias_maps_to_streamable_http(self):
        assert resolve_transport("http") == "streamable-http"
        assert resolve_transport("streamable-http") == "streamable-http"
        assert resolve_transport("streamable_http") == "streamable-http"

    def test_sse(self):
        assert resolve_transport("sse") == "sse"

    def test_case_and_whitespace_insensitive(self):
        assert resolve_transport("  STDIO ") == "stdio"
        assert resolve_transport("Http") == "streamable-http"

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError, match="Invalid WHATSAPP_MCP_TRANSPORT"):
            resolve_transport("websocket")


class TestResolvePort:
    """Tests for resolve_port()."""

    def test_default(self):
        assert resolve_port(None) == 8000
        assert resolve_port("") == 8000

    def test_valid(self):
        assert resolve_port("9000") == 9000
        assert resolve_port("1") == 1
        assert resolve_port("65535") == 65535

    def test_non_integer_raises(self):
        with pytest.raises(ValueError, match="Invalid WHATSAPP_MCP_PORT"):
            resolve_port("not-a-number")

    def test_out_of_range_raises(self):
        for value in ("0", "-1", "65536"):
            with pytest.raises(ValueError, match="Invalid WHATSAPP_MCP_PORT"):
                resolve_port(value)
