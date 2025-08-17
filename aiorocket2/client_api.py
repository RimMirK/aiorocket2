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


from .client import xRocketClient

from .tags.version import Version
from .tags.app import App
from .tags.multi_cheque import MultiCheque
from .tags.tg_invoices import TgInvoices
from .tags.withdrawal_link import WithdrawalLink
from .tags.currencies import Currencies
from .tags.health import Health


class ClientAPI(xRocketClient):
    """
    Aggregated xRocketClient with all tag methods
    """
    pass