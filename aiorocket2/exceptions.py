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


from typing import Any, Mapping, Optional

__all__ = [
    "xRocketAPIError"
]

class xRocketAPIError(Exception):
    """
    High-level API error that always carries the raw API payload and (if available) HTTP status.

    Attributes:
        message: Human-readable error message.
        payload: Raw JSON payload returned by the API.
        status: HTTP status code (if known).
    """

    def __init__(self, payload: Mapping[str, Any], status: Optional[int] = None) -> None:
        self.payload = dict(payload)
        self.status = status
        self.message = payload.get("message")
        super().__init__(self.message)
    
    def __str__(self):
        return f"API says: {self.message or '~'}\nStatus: {self.status}\nPayload: {self.payload!r}"
