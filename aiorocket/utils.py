import asyncio
import time
from typing import Optional


def make_idempotency_id() -> str:
    """
    Generate a simple idempotency identifier based on the current timestamp.

    The xRocket Pay API accepts `transferId` / `withdrawalId` for idempotency.
    """
    return str(time.time())


async def backoff_sleep(attempt: int, base: float) -> None:
    """
    Sleep using exponential backoff for the given attempt number (0-based).
    """
    delay = base * (2 ** attempt)
    await asyncio.sleep(delay)
