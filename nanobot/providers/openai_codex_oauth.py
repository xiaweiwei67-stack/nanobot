"""Small OpenAI Codex OAuth wrappers."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Callable
from contextlib import contextmanager

_PROXY_ENV_KEYS = ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy")
_PROXY_ENV_LOCK = asyncio.Lock()


@contextmanager
def _oauth_cli_kit_proxy_env(proxy: str | None):
    proxy = proxy.strip() if proxy else ""
    if not proxy:
        yield
        return

    # ponytail: oauth_cli_kit has no proxy parameter; switch to that when upstream adds one.
    original = {key: os.environ.get(key) for key in _PROXY_ENV_KEYS}
    for key in _PROXY_ENV_KEYS:
        os.environ[key] = proxy
    try:
        yield
    finally:
        for key, value in original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def get_codex_oauth_token(*, proxy: str | None = None):
    from oauth_cli_kit import get_token

    with _oauth_cli_kit_proxy_env(proxy):
        return get_token()


async def get_codex_oauth_token_async(*, proxy: str | None = None):
    from oauth_cli_kit import get_token

    if not proxy:
        return await asyncio.to_thread(get_token)
    async with _PROXY_ENV_LOCK:
        with _oauth_cli_kit_proxy_env(proxy):
            return await asyncio.to_thread(get_token)


def login_openai_codex_interactive(
    *,
    print_fn: Callable[[str], None],
    prompt_fn: Callable[[str], str],
    proxy: str | None = None,
):
    from oauth_cli_kit import login_oauth_interactive

    with _oauth_cli_kit_proxy_env(proxy):
        return login_oauth_interactive(print_fn=print_fn, prompt_fn=prompt_fn)
