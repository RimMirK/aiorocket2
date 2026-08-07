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

"""
Tag withdrawal-link from the API
"""

from typing import Optional
from ..enums import Network
from ..exceptions import xRocketAPIError


class WithdrawalLink:
    """
    Tag Withdrawal-link from the API
    """
    async def get_withdrawal_link(
        self,
        currency: str,
        network: Network,
        address: str,
        amount: float = 0,
        comment: str = None,
        platform: str = None
    ) -> Optional[str]:
        """Get a withdrawal link for on-chain withdrawals.

        Args:
            currency (str): Currency code (use :meth:`xRocketClient.get_available_currencies`).
            network (Network): ``Network`` enum member (e.g. ``Network.TON``).
            address (str): Target on-chain address.
            amount (float): Optional withdrawal amount (default ``0``).
            comment (str): Optional comment attached to withdrawal.
            platform (str): Optional platform identifier.

        Returns:
            Optional[str]: Telegram application link for withdrawal.

        Raises:
            xRocketAPIError: If the API returns an error or no link is available.

        Example:

            >>> from aiorocket2.enums import Network
            >>> async with xRocketClient(api_key="KEY") as client:
            ...     link = await client.get_withdrawal_link(currency="TON", network=Network.TON, address="EQ...", amount=0.1)
            ...     print(link)
        """
        params = {
            'currency': currency,
            'network': network.value,
            'address': address,
            'amount': amount
        }
        if comment:
            params['comment'] = comment
        if platform:
            params['platform'] = platform
            
        r = await self._request("GET", "withdrawal-link", params=params)
        link = r.get('data', {}).get('telegramAppLink')
        if link:
            return link
        raise xRocketAPIError(r)
