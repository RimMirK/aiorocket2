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
"""Health tag — quick API health checks.

Simple helper to check upstream service status. This is useful for lightweight
monitoring or readiness checks that do not require authentication.
"""

from ..enums import Status


class Health:
    """
    Tag health from the API
    """

    async def check_health(self) -> Status:
        """Return API status as a :class:`aiorocket2.enums.Status` enum.

        Returns:
            Status: Service status reported by the API.
        """
        r = await self._request("GET", "health", require_success=False)
        return Status(r.get('status') or "UNKNOWN")
    