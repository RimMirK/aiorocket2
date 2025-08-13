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
