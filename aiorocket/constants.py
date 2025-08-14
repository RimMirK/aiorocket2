"""
Constants used by the aiorocket package.
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
DEFAULT_USER_AGENT: str = "aiorocket/2.0 (+https://github.com/RimMirK/aiorocket)"
