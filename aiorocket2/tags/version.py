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

"""Version tag — API version information.

This tag exposes a single helper to retrieve the upstream API version and can
be used as a lightweight healthcheck.
"""

class Version:
    """
    Tag version from the API
    """
    async def get_version(self) -> str:
        """Return the upstream API version string.

        Returns:
            str: Version string, for example ``"1.3.1"``.

        Example::

            version = await client.get_version()
        """
        r = await self._request("GET", "version", require_auth_header=False, require_success=False)
        return str(r.get("version"))
