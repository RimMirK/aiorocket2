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


from typing import List, Optional, Union

from ..exceptions import xRocketAPIError

from ..enums import Country
from ..models import Cheque, PaginatedCheque


class MultiCheque:
    async def create_multi_cheque(
        self,
        currency: str,
        cheque_per_user: float,
        users_number: int,
        ref_program: int,
        password: str = None,
        description: str = None,
        send_notifications: bool = True,
        enable_captcha: bool = True,
        telegram_resources_ids: List[Union[int, str]] = None,
        for_premium: bool = False,
        linked_wallet: bool = False,
        disabled_languages: List[str] = None,
        enabled_countries: List["Country"] = None
    ) -> Cheque:
        """Create a multi-cheque (voucher) for multiple activations.

        Args:
            currency (str): Currency code such as ``"TON"``. Use
                :meth:`xRocketClient.get_available_currencies` to list valid currencies.
            cheque_per_user (float): Amount reserved per activation (up to 9 decimals).
            users_number (int): Number of activations (integer, minimum 1).
            ref_program (int): Referral program percentage (0-100).
            password (str): Optional password for the cheque (max length 100).
            description (str): Optional description for the cheque (max length 1000).
            send_notifications (bool): Whether to send activation notifications.
            enable_captcha (bool): Enable captcha for activation flow.
            telegram_resources_ids (List[Union[int, str]]): Telegram resource ids (group/channel ids).
            for_premium (bool): Restrict activation to Telegram Premium users.
            linked_wallet (bool): Require linked wallet for activation.
            disabled_languages (List[str]): Languages to disable.
            enabled_countries (List[Country]): Pass members of the ``Country`` enum
                (for example ``[Country.US, Country.GB]``). The client converts enums
                to their API string values internally.

        Returns:
            Cheque: Model representing created cheque.

        Raises:
            xRocketAPIError: On API or validation errors.

        Example:

            >>> from aiorocket2.enums import Country
            >>> async with xRocketClient(api_key="KEY") as client:
            ...     chk = await client.create_multi_cheque(currency="TON", cheque_per_user=0.001, users_number=50, ref_program=0, enabled_countries=[Country.US])
            ...     print(chk.id, chk.inviteUrl)
        """
        payload = {
            "currency": currency,
            "chequePerUser": cheque_per_user,
            "usersNumber": users_number,
            "refProgram": ref_program,
            "password": password,
            "description": description,
            "sendNotifications": send_notifications,
            "enableCaptcha": enable_captcha,
            "telegramResourcesIds": telegram_resources_ids,
            "forPremium": for_premium,
            "linkedWallet": linked_wallet,
            "disabledLanguages": disabled_languages,
            "enabledCountries": [country.value for country in (enabled_countries or [])]
        }
        r = await self._request("POST", "multi-cheque", json=payload)
        return Cheque.from_api(r['data'])

    async def get_multi_cheques(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> PaginatedCheque:
        """Return paginated list of multi-cheques.

        Args:
            limit (int): Number of items to return (1-1000). Default 100.
            offset (int): Result offset (>=0). Default 0.

        Returns:
            PaginatedCheque: Paginated result with `results` containing :class:`Cheque`.

        Raises:
            xRocketAPIError: If the API returns an error.
        """
        r = await self._request('GET', 'multi-cheque', params={"limit": limit, "offset": offset})
        return PaginatedCheque.from_api(r['data'])

    async def get_multi_cheque(
        self,
        cheque_id: int
    ) -> Cheque:
        """Return details for a single multi-cheque.

        Args:
            cheque_id (int): Cheque identifier.

        Returns:
            Cheque: Parsed cheque model.

        Raises:
            xRocketAPIError: If the cheque is not found or API reports an error.
        """
        r = await self._request("GET", f"multi-cheque/{cheque_id}")
        return Cheque.from_api(r["data"])

    async def edit_multi_cheque(
        self,
        cheque_id: int,
        password: str = None,
        description: str = None,
        send_notifications: bool = None,
        enable_captcha: bool = None,
        telegram_resources_ids: List[Union[int, str]] = None,
        for_premium: bool = None,
        linked_wallet: bool = None,
        disabled_languages: List[str] = None,
        enabled_countries: List["Country"] = None
    ) -> Cheque:
        """Update properties of an existing multi-cheque.

        Args:
            cheque_id (int): Cheque identifier.
            password (str): Optional password (max 100 chars).
            description (str): Optional description (max 1000 chars).
            send_notifications (bool): Whether to send activation notifications.
            enable_captcha (bool): Enable captcha for activation.
            telegram_resources_ids (List[Union[int,str]]): IDs of telegram resources.
            for_premium (bool): Restrict activation to Telegram Premium users.
            linked_wallet (bool): Require linked wallet for activation.
            disabled_languages (List[str]): Languages to disable.
            enabled_countries (List[Country]): Allowed countries.

        Returns:
            Cheque: Updated cheque model.

        Raises:
            xRocketAPIError: On validation or API errors.
        """
        payload = {
            "password": password,
            "description": description,
            "sendNotifications": send_notifications,
            "enableCaptcha": enable_captcha,
            "telegramResourcesIds": telegram_resources_ids,
            "forPremium": for_premium,
            "linkedWallet": linked_wallet,
            "disabledLanguages": disabled_languages,
            "enabledCountries": [country.value for country in (enabled_countries or [])]
        }

        r = await self._request("PUT", f"multi-cheque/{cheque_id}", json=payload)
        return Cheque.from_api(r["data"])

    async def delete_multi_cheque(self, cheque_id: str) -> True:
        """
        Delete a multi-cheque by id.

        Args:
            cheque_id (str): Cheque identifier.

        Returns:
            True: On success.

        Raises:
            xRocketAPIError: If deletion fails.
        """
        r = await self._request("DELETE", f"multi-cheque/{cheque_id}")
        return r['success'] is True
