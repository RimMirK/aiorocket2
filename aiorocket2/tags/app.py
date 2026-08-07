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

"""App tag — methods that operate on application-level resources.

This module exposes operations such as balance inspection, internal transfers
and withdrawals. Methods return model instances from :mod:`aiorocket2.models`.

Examples
--------

>>> async with xRocketClient(api_key="KEY") as client:
>>>     info = await client.get_info()
>>>     print(info.balances)
"""

from typing import Any, Dict, List, Optional

from ..enums import Network, WithdrawalStatus
from ..models import Info, Transfer, Withdrawal, WithdrawalCoin


class App:
    """
    Tag App from the API
    """    
    async def get_info(self) -> Info:
        """Return information about the current application.

        Returns:
            Info: Application info including balances.

        Raises:
            xRocketAPIError: On API or network errors.
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
        Make an internal transfer to a Telegram user.

        Args:
            tg_user_id (int): Target Telegram user id. If unknown to the API the
                request will fail with a 400 error.
            currency (str): Currency code (see :meth:`Currencies.get_available_currencies`).
            amount (float): Transfer amount (up to 9 decimals).
            transfer_id (str): Idempotency/unique transfer id in your system to
                prevent duplicate transfers.
            description (str): Optional transfer description.

        Returns:
            Transfer: Model with transfer details.
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
        """Create a withdrawal to an external address.

        Args:
            network (Network): Network code.
            address (str): Withdrawal address.
            currency (str): Currency code.
            amount (float): Amount to withdraw (up to 9 decimals).
            withdrawal_id (str): Unique idempotency identifier (<=50 chars).
            comment (str): Optional comment (<=50 chars).

        Returns:
            Withdrawal: Created withdrawal record.

        Raises:
            xRocketAPIError: On validation or API errors.
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
        """Return withdrawal details by id.

        Args:
            withdrawal_id (str): Unique withdrawal id used in your system.

        Returns:
            Withdrawal: Withdrawal details.

        Raises:
            xRocketAPIError: If the withdrawal is not found or API returns error.
        """
        
        r = await self._request("GET", f"app/withdrawal/status/{withdrawal_id}")
        return Withdrawal.from_api(r['data'])
    
    async def get_withdrawal_status(
        self, withdrawal_id: str
    ) -> WithdrawalStatus:
        """Return status for a withdrawal.

        This is a thin helper around :meth:`get_withdrawal` that returns the
        parsed :class:`WithdrawalStatus` enum.

        Args:
            withdrawal_id (str): Unique withdrawal id.

        Returns:
            WithdrawalStatus: Current status.

        Raises:
            xRocketAPIError: If the API call fails.
        """

        return (await self.get_withdrawal(withdrawal_id=withdrawal_id)).status

    async def get_withdrawal_fees(
        self, currency: Optional[str] = None
    ) -> List[WithdrawalCoin]:
        """Return withdrawal fee information for supported coins.

        Args:
            currency (str): Optional currency code to filter fees by.

        Returns:
            List[WithdrawalCoin]: Fee metadata per coin.

        Raises:
            xRocketAPIError: If the API returns an error.
        """
        r = await self._request('GET', 'app/withdrawal/fees', params={'currency': currency} if currency else None)
        return [WithdrawalCoin.from_api(data) for data in r['data']]
