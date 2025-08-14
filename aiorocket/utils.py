#  aiorocket - Asynchronous Python client for xRocket Pay API
#  Copyright (C) 2025-present RimMirK
#
#  This file is part of aiorocket.
#
#  aiorocket is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3 of the License.
#
#  aiorocket is an independent, unofficial client library.
#  It is a near one-to-one reflection of the xRocket Pay API:
#  all methods, parameters, objects and enums are implemented.
#  If something does not work as expected, please open an issue.
#
#  You should have received a copy of the GNU General Public License
#  along with aiorocket.  If not, see the LICENSE file.
#
#  Repository: https://github.com/RimMirK/aiorocket
#  Documentation: https://aiorocket.rimmirk.pp.ua
#  Telegram: @RimMirK



import asyncio
import time

__all__ = [
    "generate_idempotency_id",
    "gii",
    "backoff_sleep"
]

def generate_idempotency_id() -> str:
    """
    Generate a simple idempotency identifier based on the current timestamp.

    The xRocket Pay API accepts `transferId` / `withdrawalId` for idempotency.
    """
    return str(time.time())

gii = generate_idempotency_id

async def backoff_sleep(attempt: int, base: float) -> None:
    """
    Sleep using exponential backoff for the given attempt number (0-based).
    """
    delay = base * (2 ** attempt)
    await asyncio.sleep(delay)
