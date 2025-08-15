#  aiorocket2 - Asynchronous Python client for xRocket Pay API
#  Copyright (C) 2025-present RimMirK
#
#  This file is part of aiorocket2.
#
#  aiorocket2 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3 of the License.
#
#  aiorocket2 is an independent, unofficial client library.
#  It is a near one-to-one reflection of the xRocket Pay API:
#  all methods, parameters, objects and enums are implemented.
#  If something does not work as expected, please open an issue.
#
#  You should have received a copy of the GNU General Public License
#  along with aiorocket2.  If not, see the LICENSE file.
#
#  Repository: https://github.com/RimMirK/aiorocket2
#  Documentation: https://aiorocket2.rimmirk.pp.ua
#  Telegram: @RimMirK

"""
TODO
"""

from __future__ import annotations

import asyncio
from typing import Any, Mapping, Optional

import aiohttp


from .constants import (
    BASEURL_MAINNET, BASEURL_TESTNET,
    DEFAULT_BACKOFF_BASE, DEFAULT_RETRIES,
    DEFAULT_TIMEOUT, DEFAULT_USER_AGENT
)
from .exceptions import xRocketAPIError
from .tags import Tags
from .utils import backoff_sleep


__all__ = [
    "xRocketClient"
]


class xRocketClient(Tags):
    """
    Asynchronous client for the xRocket Pay API.
    """

    def __init__(
        self,
        api_key: str,
        *,
        testnet: bool = False,
        base_url: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        backoff_base: float = DEFAULT_BACKOFF_BASE,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        """
        Initialize the client.

        Args:
            api_key: Your xRocket Pay API key.
            testnet: If True, use the staging/test environment.
            base_url: Optional override for the base API URL.
            session: Optional aiohttp session to reuse.
            timeout: aiohttp total timeout (seconds).
            retries: Number of retries for network/5xx errors.
            backoff_base: Base delay for exponential backoff (seconds).
            user_agent: Custom User-Agent header value.
        """
        self.base_url = (base_url or (BASEURL_TESTNET if testnet else BASEURL_MAINNET)).rstrip("/")
        self.api_key = api_key
        self._own_session = session is None
        self.session = session or aiohttp.ClientSession()
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.retries = max(0, retries)
        self.backoff_base = max(0.0, backoff_base)
        self._auth_headers = {
            "Rocket-Pay-Key": api_key,
            "User-Agent": user_agent,
            "Accept": "application/json",
        }
        self._noauth_headers = {
            "User-Agent": user_agent,
            "Accept": "application/json",
        }

    async def __aenter__(self) -> "xRocketClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Close the underlying aiohttp session if it was created by this client."""
        if self._own_session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Mapping[str, Any]] = None,
        require_auth_header: bool = True,
        require_success: bool = True
    ) -> dict:
        """
        Send an HTTP request with retries and consistent error handling.

        Args:
            method: HTTP verb (GET/POST/PUT/DELETE).
            endpoint: Path after the base URL (e.g., "app/info").
            params: Optional query string parameters.
            json: Optional JSON body.
            require_auth_header: Whether to include `Rocket-Pay-Key`.

        Returns:
            Parsed JSON body as a dictionary.

        Raises:
            xRocketAPIError: For non-2xx responses or payloads with success=false.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._auth_headers if require_auth_header else self._noauth_headers

        attempt = 0
        while True:
            try:
                async with self.session.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    headers=headers,
                    timeout=self.timeout,
                ) as resp:
                    status = resp.status
                    try:
                        payload = await resp.json()
                    except Exception:
                        text = await resp.text()
                        raise xRocketAPIError(
                            {"message": f"Non-JSON response: {text[:300]}"},
                            status=status
                        )

                    if require_success and not payload.get("success", False):
                        raise xRocketAPIError(payload, status=status)
                    return payload
            except (aiohttp.ClientError, asyncio.TimeoutError, xRocketAPIError) as e:
                # Retry only for network errors and 5xx RocketAPIError
                retryable = isinstance(e, (aiohttp.ClientError, asyncio.TimeoutError)) or (
                    isinstance(e, xRocketAPIError) and (getattr(e, "status", 0) >= 500)
                )
                if not retryable or attempt >= self.retries:
                    if isinstance(e, xRocketAPIError):
                        raise
                    raise xRocketAPIError({"message": str(e)}, status=None)
                await backoff_sleep(attempt, self.backoff_base)
                attempt += 1
