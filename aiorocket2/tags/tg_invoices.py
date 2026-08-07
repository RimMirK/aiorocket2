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
Tag tg-invoices from the API
"""

from ..models import Invoice, PaginatedInvoice


class TgInvoices:
    """
    Tag tg-invoices from the API
    """

    async def create_invoice(
        self,
        currency: str,
        amount: float = None,
        min_payment: float = None,
        num_payments: int = 1,
        description: str = None,
        hidden_message: str = None,
        comments_enabled: bool = False,
        callback_url: str = None,
        payload: str = None,
        expired_in: int = 0,
        platform_id: str = None,
    ) -> Invoice:
        """
            amount (float): Optional. Invoice amount. 9 decimal places, others cut off. Minimum 0. Maximum 1_000_000
            min_payment (float): Optional. Min payment only for multi invoice if invoice amount is None. Minimum 0. Maximum 1_000_000
            num_payments (int): Optional. Num payments for invoice. Minimum 0. Maximum 1_000_000
            description (str): Optional. Description for invoice. Maximum 1000
            hidden_message (str): Optional. Hidden message after invoice is paid. Maximum 2000
            comments_enabled (bool): Optional. Allow comments. Default False
            callback_url (str): Optional. Url for Return button after invoice is paid. Maximum 500
            payload (str): Optional. Any data. Invisible to user, will be returned in callback. Maximum 4000
            expired_in (int): Optional. Invoice expire time in seconds, max 1 day, 0 - none expired. Minimum 0. Maximum 86400. Default 0
            platform_id (str): Optional. Platform identifier
        
        Create invoice.

        Args:
            currency (str): Currency code, for example ``"TON"``. Use
                ``xRocketClient.get_available_currencies()`` to list valid currencies.
            amount (float): Optional fixed invoice amount. Use decimal precision up to
                9 fractional places; values are truncated by the API.
            min_payment (float): Optional minimum payment for multi-pay invoices.
            num_payments (int): Number of allowed partial payments (default ``1``).
            description (str): Visible description for the payer (max 1000 chars).
            hidden_message (str): Message shown to the payer after successful payment.
            comments_enabled (bool): Allow comments on the invoice.
            callback_url (str): Return/callback URL (optional).
            payload (str): Opaque string returned in callbacks — useful for your internal IDs.
            expired_in (int): Expiry in seconds (``0`` — never expire).
            platform_id (str): Optional platform identifier.

        Returns:
            Invoice: Parsed invoice model returned by the API.

        Raises:
            xRocketAPIError: When API returns non-success or for network errors.

        Notes:
            - Prefer passing enum members where available; for currency codes the
              current API accepts strings, but using a canonical source reduces typos.
            - For accounting-sensitive flows consider using ``decimal.Decimal`` to
              construct amounts before converting to ``float``.

        Example:
            >>> async with xRocketClient(api_key="KEY") as client:
            ...     inv = await client.create_invoice(currency="TON", amount=0.005, description="Tip")
            ...     print(inv.id, inv.url)
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
        """Return paginated list of invoices.

        Args:
            limit (int): Number of items to return (1-1000). Default 100.
            offset (int): Result offset (>=0). Default 0.

        Returns:
            PaginatedInvoice: Paginated result with `results` list of :class:`Invoice`.

        Raises:
            xRocketAPIError: If the API returns an error.
        """
        r = await self._request('GET', 'tg-invoices', params={"limit": limit, "offset": offset})
        return PaginatedInvoice.from_api(r['data'])

    async def get_invoice(
        self,
        invoice_id: int
    ) -> Invoice:
        """Return a single invoice by id.

        Args:
            invoice_id (int): Invoice identifier.

        Returns:
            Invoice: Parsed invoice model.

        Raises:
            xRocketAPIError: If invoice is not found or API error occurs.
        """
        r = await self._request("GET", f"tg-invoices/{invoice_id}")
        return Invoice.from_api(r["data"])

    async def delete_invoice(
        self,
        invoice_id: int
    ) -> True:
        """Delete an invoice.

        Args:
            invoice_id (int): Invoice identifier.

        Returns:
            True: On successful deletion.

        Raises:
            xRocketAPIError: If deletion fails.
        """
        r = await self._request("DELETE", f"tg-invoices/{invoice_id}")
        return r['success'] is True
