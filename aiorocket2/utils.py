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

"""Utility helpers used across the package.

The helpers are intentionally small and focused: id generation for idempotency
and a simple exponential backoff helper used by network retry logic.
"""

import asyncio
import time

__all__ = [
    "generate_idempotency_id",
    "gii",
    "backoff_sleep"
]

def generate_idempotency_id() -> str:
    """Generate a simple idempotency identifier based on the current timestamp.

    Returns:
        str: A timestamp-based string suitable as a quick idempotency id.

    Note:
        This function is intentionally simple. For production systems consider a
        stronger idempotency/nonce strategy (UUIDs or HMAC-based ids).
    """
    return str(time.time())

gii = generate_idempotency_id

async def backoff_sleep(attempt: int, base: float) -> None:
    """Asynchronously sleep using exponential backoff.

    Args:
        attempt (int): 0-based attempt number. The delay grows as ``base * 2**attempt``.
        base (float): Base delay in seconds for attempt 0.

    Example::

        await backoff_sleep(attempt=2, base=0.25)  # sleeps 1.0s
    """
    delay = base * (2 ** attempt)
    await asyncio.sleep(delay)
