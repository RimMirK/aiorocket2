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
aiorocket2 — idiomatic async Python client for the xRocket Pay API.
"""
from .version import __version__
__author__ = "RimMirK"
__license__ = "GPL-3.0"
__copyright__ = "Copyright (c) 2025 RimMirK"
__title__ = "aiorocket2"
__summary__ = "Async client for xRocket Pay API"
__url__ = "https://github.com/RimMirK/aiorocket2"
__docs__ = "https://aiorocket2.rimmirk.pp.ua"
__email__ = "me@RimMirK.pp.ua"
__maintainer__ = "RimMirK"
__credits__ = ["Sovenok-Hacker", "RimMirK"]
__status__ = "Alpha"
__keywords__ = ['crypto', 'telegram', 'async', 'asynchronous',
                'payments', 'rocket', 'cryptocurrency', 'asyncio',
                'crypto-bot', 'cryptopayments', 'xrocket', 'aiorocket2']
__requires__ = ["aiohttps"] # зависимости (редко указывают прямо в коде)
__python_requires__ = ">=3.8"    # минимальная версия питона


from .client import *
from .client import __all__ as __client_all__
from .exceptions import *
from .exceptions import __all__ as __exceptions_all__
from .models import *
from .models import __all__ as __models_all__
from .enums import *
from .enums import __all__ as __enums_all__
from .utils import *
from .utils import __all__ as __utils_all__

__all__ = __client_all__ + __exceptions_all__ + __models_all__ + __enums_all__ + __utils_all__ # type: ignore