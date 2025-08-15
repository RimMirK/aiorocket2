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


from typing import List

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
        telegram_resources_ids: List[int|str] = None,
        for_premium: bool = False,
        linked_wallet: bool = False,
        disabled_languages: List[str] = None,
        enabled_countries: List[Country] = None
    ) -> Cheque:
        """
        Create multi-cheque

        Args:
            currency (str): Currency of transfer, info `xRocketClient.get_available_currencies()`
            cheque_per_user (float): Cheque amount for one user. 9 decimal places, others cut off
            users_number (int): Number of users to save multicheque. 0 decimal places. Minimum 1
            ref_program (int): Referral program percentage (%). 0 decimal places. Minimum 0. Maximum 100
            password (str): Optional. Password for cheque. Max length 100
            description (str): Optional. Description for cheque. Max length 1000
            send_notifications (bool): Optional. Send notifications about activations. Default True
            enable_captcha (bool): Optional. Enable captcha. Default True
            telegram_resources_ids (List of int or str): IDs of telegram resources (groups, channels, private groups)
            for_premium (bool): Optional. Only users with Telegram Premium can activate this cheque. Default False
            linked_wallet (bool): Optional. Only users with linked wallet can activate this cheque. Default False
            disabled_languages (List of str): Optional. Disable languages
            enabled_countries (List of Country): Optional. Enabled countries

        Returns:
            Cheque: 
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
        """
        Get list of multi-cheques
        
        Args:
            limit (int): Minimum 1. Maximum 1000. Default 100
            offset (int): Minimum 0. Default 0
            
        Returns:
            PaginatedCheque:
        """
        r = await self._request('GET', 'multi-cheque', params={"limit": limit, "offset": offset})
        return PaginatedCheque.from_api(r['data'])

    async def get_multi_cheque(
        self,
        cheque_id: int
    ) -> Cheque:
        """
        Get multi-cheque info
        
        Args:
            cheque_id (str): Cheque ID
            
        Returns:
            Cheque: 
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
        telegram_resources_ids: List[int|str] = None,
        for_premium: bool = None,
        linked_wallet: bool = None,
        disabled_languages: List[str] = None,
        enabled_countries: List[Country] = None
    ) -> Cheque:
        """
        Edit multi-cheque
        
        Args:
            cheque_id (int):
            password: (str): Optional. Password for cheque. Max lenght 100
            description (str): Optional. Description for cheque. Max lenght 1000
            send_notifications (bool): Optional. Send notifications about activations. Default True
            enable_captcha (bool): Optional. Enable captcha. Default True
            telegram_resources_ids (List of int or str): IDs of telegram resources (groups, channels, private groups)
            for_premium (bool): Optional. Only users with Telegram Premium can activate this cheque. Default False
            linked_wallet (bool): Optional. Only users with linked wallet can activate this cheque. Default False
            disabled_languages (List of str): Optional. Disable languages
            enabled_countries (List of Country): Optional. Enabled countries

        Returns:
            Cheque: 
        
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
        Delete multi-cheque
        
        Args:
            cheque_id (str): Cheque ID
            
        Returns:
            True: on success, otherwise raises xRocketAPIError
        """
        r = await self._request("DELETE", f"multi-cheque/{cheque_id}")
        return r['success'] == True
