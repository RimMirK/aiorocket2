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

"""Tag composition for aiorocket2.

The upstream API groups endpoints by *tags* (for example ``app``,
``tg-invoices``, ``multi-cheque``). Each tag is implemented as a mixin-like
class in this package and then composed into the `Tags` helper. The main
client :class:`aiorocket2.client.xRocketClient` inherits from ``Tags`` to
expose all convenience methods on the client instance.

Available tags
--------------
- ``Version`` — API version helpers
- ``App`` — application-level operations (balance, transfer, withdrawals)
- ``MultiCheque`` — multi-cheque (voucher) endpoints
- ``TgInvoices`` — invoice creation and retrieval
- ``WithdrawalLink`` — on-chain withdrawal link helper
- ``Currencies`` — currency listing helper
- ``Health`` — lightweight health check
"""

from .version import Version
from .app import App
from .multi_cheque import MultiCheque
from .tg_invoices import TgInvoices
from .withdrawal_link import WithdrawalLink
from .currencies import Currencies
from .health import Health

class Tags(
    Version, App, MultiCheque,
    TgInvoices, WithdrawalLink,
    Currencies, Health
):
    """
    General class to join all tags together
    """
    