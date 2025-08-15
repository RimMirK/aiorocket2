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
Constants used by the aiorocket2 package.
"""

__all__ = [
    "BASEURL_MAINNET",
    "BASEURL_TESTNET", 
    "DEFAULT_TIMEOUT",
    "DEFAULT_RETRIES",
    "DEFAULT_BACKOFF_BASE",
    "DEFAULT_USER_AGENT"
]

BASEURL_MAINNET: str = "https://pay.xrocket.tg"
BASEURL_TESTNET: str = "https://pay.testnet.xrocket.tg"

DEFAULT_TIMEOUT: float = 30.0          # seconds (aiohttp total timeout)
DEFAULT_RETRIES: int = 3               # network/5xx retries
DEFAULT_BACKOFF_BASE: float = 0.25     # seconds
DEFAULT_USER_AGENT: str = "aiorocket2/2.0 (+https://github.com/RimMirK/aiorocket2)"
