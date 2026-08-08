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
#  Documentation: https://docs.aiorocket2.rimmirk.dev
#  Telegram: @RimMirK
"""Currencies tag — list available currencies.

Provides a convenience method to fetch the list of currencies supported by
the upstream API. This call is safe to use without authentication.

Example::

    async with xRocketClient(api_key="KEY") as client:
        currencies = await client.get_available_currencies()
        for c in currencies:
            print(c.currency, c.min_transfer)
"""

from typing import List

from ..models import Currency


class Currencies:
    """Tag currencies from the API."""
    
    async def get_available_currencies(self) -> List[Currency]:
        """Return available currencies from the API.

        Returns:
            List[Currency]: Parsed list of currency models.

        Raises:
            xRocketAPIError: If the request fails.
        """
        r = await self._request("GET", "currencies/available", require_auth_header=False)
        return [Currency.from_api(c) for c in r["data"].get("results", [])]
