#  aiorocket - Asynchronous Python client for xRocket Pay API
#  Copyright (C) 2025-present RimMirK
#
#  This file is part of aiorocket.
#
#  aiorocket is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3 of the License.
#
#  aiorocket is an independent, unofficial client library.
#  It is a near one-to-one reflection of the xRocket Pay API:
#  all methods, parameters, objects and enums are implemented.
#  If something does not work as expected, please open an issue.
#
#  You should have received a copy of the GNU General Public License
#  along with aiorocket.  If not, see the LICENSE file.
#
#  Repository: https://github.com/RimMirK/aiorocket
#  Documentation: https://aiorocket.rimmirk.pp.ua
#  Telegram: @RimMirK

from ..models import Invoice, PaginatedInvoice


class TgInvoices:
    

    async def create_invoice(
        self,
        amount: float,
        min_payment: float,
        num_payments: int,
        currency: str,
        description: str = None,
        hidden_message: str = None,
        comments_enabled: bool = False,
        callback_url: str = None,
        payload: str = None,
        expired_in: int = 0,
        platform_id: str = None,
    ) -> Invoice:
        """
        Create invoice
        
        Args:
            amount (float): Invoice amount. 9 decimal places, others cut off. Minimum 0. Maximum 1_000_000
            min_payment (float): Min payment only for multi invoice if invoice amount is None. Minimum 0. Maximum 1_000_000
            num_payments (int): Num payments for invoice. Minimum 0. Maximum 1_000_000
            currency (str): Currency of transfer, info `xRocketClient.get_available_currencies()`
            description (str): Optional. Description for invoice. Maximum 1000
            hidden_message (str): Optional. Hidden message after invoice is paid. Maximum 2000
            comments_enabled (bool): Optional. Allow comments. Default False
            callback_url (str): Optional. Url for Return button after invoice is paid. Maximum 500
            payload (str): Optional. Any data. Invisible to user, will be returned in callback. Maximum 4000
            expired_in (int): Optional. Invoice expire time in seconds, max 1 day, 0 - none expired. Minimum 0. Maximum 86400. Default 0
            platform_id (str): Optional. Platform identifier
        
        Returns:
            Invoice:
        """
        api_payload = {
            "amount": amount,
            "minPayment": min_payment,
            "numPayments": num_payments,
            "currency": currency,
            "description": description, 
            "hiddenMessage": hidden_message, 
            "commentsEnabled": comments_enabled, 
            "callbackUrl": callback_url, 
            "payload": payload, 
            "expiredIn": expired_in, 
            "platformId": platform_id, 
        }
        r = await self._request("POST", "tg-invoices", json=api_payload)
        return Invoice.from_api(r["data"])

    async def get_invoices(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> PaginatedInvoice:
        """
        Get list of invoices
        
        Args:
            limit (int): Minimum 1. Maximum 1000. Default 100
            offset (int): Minimum 0. Default 0
            
        Returns:
            PaginatedInvoice:
        """
        r = await self._request('GET', 'tg-invoices', params={"limit": limit, "offset": offset})
        return PaginatedInvoice.from_api(r['data'])

    async def get_invoice(
        self,
        invoice_id: int
    ) -> Invoice:
        """
        Get invoice

        Args:
            invoice_id (str): invoice id

        Returns:
            Invoice
        """
        r = await self._request("GET", f"tg-invoices/{invoice_id}")
        return Invoice.from_api(r["data"])

    async def delete_invoice(
        self,
        invoice_id: int
    ) -> True:
        """
        Delete invoice

        Args:
            invoice_id (int):
        
        Returns:
            True: on succer otherwize raises xRocketAPIError
        """
        r = await self._request("DELETE", f"tg-invoices/{invoice_id}")
        return r['success'] == True
