"""
aiorocket — idiomatic async Python client for the xRocket Pay API.

Quickstart:
    >>> import asyncio
    >>> from aiorocket import RocketClient
    >>> async def main():
    ...     async with RocketClient("YOUR_API_KEY") as xrocket:
    ...         print(await xrocket.version())
    ...         print(await xrocket.info())
    ...         print(await xrocket.balance())
    ... 
    >>> asyncio.run(main())
    >>> # or
    >>> async def main():
    ...     xrocket = RocketClient("YOUR_API_KEY")
    ...     print(await xrocket.version())
    ...     print(await xrocket.info())
    ...     print(await xrocket.balance())
    ...
    >>> asyncio.run(main())
"""

from .client import xRocketClient
from .exceptions import xRocketAPIError
from .models import *
from .enums import *
