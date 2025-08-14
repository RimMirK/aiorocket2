from __future__ import annotations

import asyncio
from typing import Any, AsyncIterator, Dict, List, Mapping, Optional, TypedDict

import aiohttp

from .constants import (
    BASEURL_MAINNET,
    BASEURL_TESTNET,
    DEFAULT_BACKOFF_BASE,
    DEFAULT_RETRIES,
    DEFAULT_TIMEOUT,
    DEFAULT_USER_AGENT,
)
from .exceptions import xRocketAPIError
from .models import *
from .utils import *
from .enums import *


class _ApiResponse(TypedDict, total=False):
    success: bool
    message: str
    errors: list
    data: Dict | List | Any
    version: str


class xRocketClient:
    """
    Asynchronous client for the xRocket Pay API.

    This client wraps common API endpoints such as app info & balances,
    transfers and withdrawals, multi-cheques, Telegram invoices, and available
    currencies. It provides automatic retries for transient errors and
    implements a context manager for clean session handling.

    Notes:
        * Most endpoints require the `Rocket-Pay-Key` header with your API key.
        * `/version` does not require authentication.
        * This client is built around the public patterns used by xRocket Pay:
          - `GET /version`
          - `GET /app/info`
          - `POST /app/transfer`
          - `POST /app/withdrawal`
          - CRUD for `/multi-cheques`
          - CRUD for `/tg-invoices`
          - `GET /currencies/available`
        * If the official API adds new fields, you can extend the explicit
          parameters below without resorting to `**kwargs`.

    Example:
        ```python
        async with xRocketClient("YOUR_KEY") as rp:
            ver = await rp.version()
            info = await rp.info()
            bal = await rp.balance()
        ```
    """

    def __init__(
        self,
        api_key: str,
        *,
        testnet: bool = False,
        base_url: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        backoff_base: float = DEFAULT_BACKOFF_BASE,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        """
        Initialize the client.

        Args:
            api_key: Your xRocket Pay API key.
            testnet: If True, use the staging/test environment.
            base_url: Optional override for the base API URL.
            session: Optional aiohttp session to reuse.
            timeout: aiohttp total timeout (seconds).
            retries: Number of retries for network/5xx errors.
            backoff_base: Base delay for exponential backoff (seconds).
            user_agent: Custom User-Agent header value.
        """
        self.base_url = (base_url or (BASEURL_TESTNET if testnet else BASEURL_MAINNET)).rstrip("/")
        self.api_key = api_key
        self._own_session = session is None
        self.session = session or aiohttp.ClientSession()
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.retries = max(0, retries)
        self.backoff_base = max(0.0, backoff_base)
        self._auth_headers = {
            "Rocket-Pay-Key": api_key,
            "User-Agent": user_agent,
            "Accept": "application/json",
        }
        self._noauth_headers = {
            "User-Agent": user_agent,
            "Accept": "application/json",
        }

    # ---- context management ----

    async def __aenter__(self) -> "xRocketClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Close the underlying aiohttp session if it was created by this client."""
        if self._own_session:
            await self.session.close()

    # ---- low-level request helper ----

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Mapping[str, Any]] = None,
        require_auth_header: bool = True,
        require_success: bool = True
    ) -> _ApiResponse:
        """
        Send an HTTP request with retries and consistent error handling.

        Args:
            method: HTTP verb (GET/POST/PUT/DELETE).
            endpoint: Path after the base URL (e.g., "app/info").
            params: Optional query string parameters.
            json: Optional JSON body.
            require_auth_header: Whether to include `Rocket-Pay-Key`.

        Returns:
            Parsed JSON body as a dictionary.

        Raises:
            xRocketAPIError: For non-2xx responses or payloads with success=false.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._auth_headers if require_auth_header else self._noauth_headers

        attempt = 0
        while True:
            try:
                async with self.session.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    headers=headers,
                    timeout=self.timeout,
                ) as resp:
                    status = resp.status
                    try:
                        payload: _ApiResponse = await resp.json()
                    except Exception:
                        text = await resp.text()
                        raise xRocketAPIError({"message": f"Non-JSON response: {text[:300]}"},
                                             status=status)

                    if require_success and not payload.get("success", False):
                        raise xRocketAPIError(payload, status=status)
                    return payload
            except (aiohttp.ClientError, asyncio.TimeoutError, xRocketAPIError) as e:
                # Retry only for network errors and 5xx RocketAPIError
                retryable = isinstance(e, (aiohttp.ClientError, asyncio.TimeoutError)) or (
                    isinstance(e, xRocketAPIError) and (getattr(e, "status", 0) >= 500)
                )
                if not retryable or attempt >= self.retries:
                    if isinstance(e, xRocketAPIError):
                        raise
                    raise xRocketAPIError({"message": str(e)}, status=None)
                await backoff_sleep(attempt, self.backoff_base)
                attempt += 1

    # ---- api methods ----

    async def get_version(self) -> str:
        """
        Returns current version of API. You may use it as healthcheck

        Returns:
            str: Version string, e.g., "1.3.1".
        """
        r = await self._request("GET", "version", require_auth_header=False, require_success=False)
        return str(r.get("version"))

    async def get_info(self) -> Info:
        """
        Returns information about your application

        Returns:
            Info: information about your application
        """
        r = await self._request("GET", "app/info")
        return Info.from_api(r['data'])


    # =========================
    # Public API: Transfers
    # =========================

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
            cheque_id (str):
            
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

        r = await self._request("PUT", f"multi-cheques/{cheque_id}", json=payload)
        return Cheque.from_api(r["data"])

    async def delete_multi_cheque(self, cheque_id: str) -> True:
        """
        Delete multi-cheque
        
        Args:
            cheque_id (str):
            
        Returns:
            True: on success, otherwise raises xRocketAPIError
        """
        r = await self._request("DELETE", f"multi-cheques/{cheque_id}")
        return r['success'] == True



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

    async def get_invoice(self, invoice_id: int) -> Invoice:
        """
        Get a Telegram invoice by ID.
        """
        r = await self._request("GET", f"tg-invoices/{invoice_id}")
        return Invoice.from_api(r["data"])

    async def delete_invoice(self, invoice_id: int) -> None:
        """
        Delete a Telegram invoice by ID.
        """
        await self._request("DELETE", f"tg-invoices/{invoice_id}")

    async def list_invoices(self, *, limit: int = 100, offset: int = 0) -> List[Invoice]:
        """
        List invoices with pagination.
        """
        r = await self._request("GET", "tg-invoices", params={"limit": limit, "offset": offset})
        return [Invoice.from_api(i) for i in r["data"].get("results", [])]

    async def iter_invoices(self, *, page_size: int = 100, start_offset: int = 0) -> AsyncIterator[Invoice]:
        """
        Iterate over all invoices as an async generator.
        """
        offset = start_offset
        while True:
            batch = await self.list_invoices(limit=page_size, offset=offset)
            if not batch:
                return
            for inv in batch:
                yield inv
            offset += len(batch)

    # =========================
    # Public API: Currencies
    # =========================

    async def get_available_currencies(self) -> List[Currency]:
        """
        Get the list of available currencies and their operational constraints.

        Notes:
            Documentation indicates this endpoint is public; we request it without auth header.
        """
        r = await self._request("GET", "currencies/available", require_auth_header=False)
        return [Currency.from_api(c) for c in r["data"].get("results", [])]
