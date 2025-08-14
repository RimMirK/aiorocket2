"""
aiorocket — idiomatic async Python client for the xRocket Pay API.
"""
from .version import __version__
__author__ = "RimMirK"
__license__ = "GPL-3.0"
__copyright__ = "Copyright (c) 2025 RimMirK"
__title__ = "aiorocket"
__summary__ = "Async client for xRocket Pay API"
__url__ = "https://github.com/RimMirK/aiorocket"
__docs__ = "https://aiorocket.rimmirk.pp.ua"
__email__ = "me@RimMirK.pp.ua"
__maintainer__ = "RimMirK"
__credits__ = ["Sovenok-Hacker", "RimMirK"]
__status__ = "Alpha"
__keywords__ = ['crypto', 'telegram', 'async', 'asynchronous',
                'payments', 'rocket', 'cryptocurrency', 'asyncio',
                'crypto-bot', 'cryptopayments', 'xrocket', 'aiorocket']
__requires__ = ["aiohttps"] # зависимости (редко указывают прямо в коде)
__python_requires__ = ">=3.8"    # минимальная версия питона

from .client import xRocketClient
from .exceptions import xRocketAPIError
from .models import *
from .enums import *
from .utils import *
