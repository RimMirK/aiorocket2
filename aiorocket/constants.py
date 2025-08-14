"""
Constants used by the aiorocket package.
"""

BASEURL_MAINNET: str = "https://pay.xrocket.tg"
BASEURL_TESTNET: str = "https://pay.testnet.xrocket.tg"

# Networking defaults
DEFAULT_TIMEOUT: float = 30.0          # seconds (aiohttp total timeout)
DEFAULT_RETRIES: int = 3               # network/5xx retries
DEFAULT_BACKOFF_BASE: float = 0.25     # seconds
DEFAULT_USER_AGENT: str = "aiorocket/2.0 (+https://github.com/RimMirK/aiorocket)"
