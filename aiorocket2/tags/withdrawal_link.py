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

from ..enums import Network
from ..exceptions import xRocketAPIError


class WithdrawalLink:
    
    
    async def get_withdrawal_link(
        self,
        currency: str,
        network: Network,
        address: str,
        amount: float = 0,
        comment: str = None,
        platform: str = None
    ) -> str|None:
        """
        Get withdrawal link
        
        Args:
            currency (str): Currency code (get list from `xRocketClient.get_available_currencies()`)
            network (Network): Network code
            address (str): Target withdrawal address
            amount (float): Optional. Withdrawal amount. Default 0
            comment (str): Optional. Withdrawal comment
            platform (str): Optional. Platform identifier (optional, use only if provided by xRocket)
        
        Returns:
            str: Telegram app link
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
        else:
            raise xRocketAPIError(r)
