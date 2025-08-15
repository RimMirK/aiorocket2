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



from typing import Any, Dict, List, Optional

from ..enums import Network, WithdrawalStatus
from ..models import Info, Transfer, Withdrawal, WithdrawalCoin


class App:
    
    async def get_info(self) -> Info:
        """
        Returns information about your application

        Returns:
            Info: information about your application
        """
        r = await self._request("GET", "app/info")
        return Info.from_api(r['data'])

    async def send_transfer(
        self,
        tg_user_id: int,
        currency: str,
        amount: float,
        transfer_id: str,
        description: Optional[str] = None,
    ) -> Transfer:
        """
        Make transfer of funds to another user

        Args:
            tg_user_id (int): Telegram user ID. If we dont have this user in DB, we will fail transaction with error: 400 - User not found
            currency (str): Currency of transfer, info `xRocketClient.get_available_currencies()`
            amount (float): Transfer amount. 9 decimal places, others cut off
            transfer_id (str): Unique transfer ID in your system to prevent double spends
            description (str): Transfer description

        Returns:
            Transfer: 
        """
        payload: Dict[str, Any] = {
            "tgUserId": tg_user_id,
            "currency": currency,
            "amount": amount,
            "transferId": transfer_id,
            "description": description
        }

        r = await self._request("POST", "app/transfer", json=payload)
        return Transfer.from_api(r['data'])


    async def create_withdrawal(
        self,
        network: Network,
        address: str,
        currency: str,
        amount: float,
        withdrawal_id: str,
        comment: str,
    ) -> Withdrawal:
        """
        Make withdrawal of funds to external wallet
        
        Args:
            network (Network): Network code.
            address (str): Withdrawal address. E.g. `EQB1cmpxb3R-YLA3HLDV01Rx6OHpMQA_7MOglhqL2CwJx_dz`
            currency (str): Currency code
            amount (float): Withdrawal amount. 9 decimal places, others cut off
            withdrawal_id (str): Unique withdrawal ID in your system to prevent double spends. Must not be longer than 50
            comment (str): Withdrawal comment. Must not be longer than 50

        Returns:
            Withdrawal: 
        """
        payload: Dict[str, Any] = {
            "network": network,
            "address": address,
            "currency": currency,
            "amount": amount,
            "withdrawalId": withdrawal_id,
            "comment": comment
        }

        r = await self._request("POST", "app/withdrawal", json=payload)
        return Withdrawal.from_api(r['data'])

    async def get_withdrawal(
        self, withdrawal_id: str
    ) -> Withdrawal:
        """
        Returns withdrawal info
        
        Args:
            withdrawal_id (str): Unique withdrawal ID in your system.
            
        Returns:
            Withdrawal:
        """
        
        r = await self._request("GET", f"app/withdrawal/status/{withdrawal_id}")
        return Withdrawal.from_api(r['data'])
    
    async def get_withdrawal_status(
        self, withdrawal_id: str
    ) -> WithdrawalStatus:
        """
        Returns withdrawal status
        
        Args:
            withdrawal_id (str): Unique withdrawal ID in your system.
            
        Returns:
            WithdrawalStatus:
        """
        
        return (await self.get_withdrawal(withdrawal_id=withdrawal_id)).status

    async def get_withdrawal_fees(
        self, currency: Optional[str] = None
    ) -> List[WithdrawalCoin]:
        """
        Returns withdrawal fees
        
        Args:
            currency (str): Coin for get fees, optional
            
        Returns:
            List[WithdrawalCoin]: 
        """
        r = await self._request('GET', 'app/withdrawal/fees', params={'currency': currency} if currency else None)
        return [WithdrawalCoin.from_api(data) for data in r['data']]
