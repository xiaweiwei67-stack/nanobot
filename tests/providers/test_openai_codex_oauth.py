from __future__ import annotations

import os
from types import SimpleNamespace

import pytest

from nanobot.providers import openai_codex_oauth


def test_get_token_uses_temporary_proxy_env(monkeypatch) -> None:
    import oauth_cli_kit

    proxy = "http://127.0.0.1:23458"
    monkeypatch.setenv("HTTP_PROXY", "http://original-http.example:8080")
    monkeypatch.delenv("HTTPS_PROXY", raising=False)
    seen: dict[str, str | None] = {}

    def fake_get_token():
        seen["http"] = os.environ.get("HTTP_PROXY")
        seen["https"] = os.environ.get("HTTPS_PROXY")
        return SimpleNamespace(access="access-token", account_id="acct")

    monkeypatch.setattr(oauth_cli_kit, "get_token", fake_get_token)

    token = openai_codex_oauth.get_codex_oauth_token(proxy=proxy)

    assert token.access == "access-token"
    assert seen == {"http": proxy, "https": proxy}
    assert os.environ["HTTP_PROXY"] == "http://original-http.example:8080"
    assert "HTTPS_PROXY" not in os.environ


@pytest.mark.asyncio
async def test_async_get_token_uses_temporary_proxy_env(monkeypatch) -> None:
    import oauth_cli_kit

    proxy = "http://127.0.0.1:23458"
    monkeypatch.setenv("HTTP_PROXY", "http://original-http.example:8080")
    monkeypatch.delenv("HTTPS_PROXY", raising=False)
    seen: dict[str, str | None] = {}

    def fake_get_token():
        seen["http"] = os.environ.get("HTTP_PROXY")
        seen["https"] = os.environ.get("HTTPS_PROXY")
        return SimpleNamespace(access="access-token", account_id="acct")

    monkeypatch.setattr(oauth_cli_kit, "get_token", fake_get_token)

    token = await openai_codex_oauth.get_codex_oauth_token_async(proxy=proxy)

    assert token.access == "access-token"
    assert seen == {"http": proxy, "https": proxy}
    assert os.environ["HTTP_PROXY"] == "http://original-http.example:8080"
    assert "HTTPS_PROXY" not in os.environ
