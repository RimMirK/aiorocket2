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
from .utils import backoff_sleep, make_idempotency_id


class _ApiResponse(TypedDict, total=False):
    success: bool
    message: str
    errors: list
    data: Any
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
        *,
        tg_user_id: int,
        currency: Optional[str] = "TONCOIN",
        amount: float,
        transfer_id: str,
        description: Optional[str] = None,
    ) -> Transfer:
        """
        Make transfer of funds to another user

        Args:
            tg_user_id (int): Telegram user ID. If we dont have this user in DB, we will fail transaction with error: 400 - User not found
            currency (str): Currency of transfer, info /currencies/available
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
        *,
        network: str,
        address: str,
        currency: str,
        amount: float,
        withdrawal_id: str,
        comment: str,
    ) -> Withdrawal:
        """
        Make withdrawal of funds to external wallet
        
        Args:
            network (str): Network code. Should be one of: `TON`, `BSC`, `ETH`, `BTC`, `TRX`, `SOL`.
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
        r = await self._request("GET", f"app/withdrawal/status/{withdrawal_id}")
        return Withdrawal.from_api(r['data'])
    
    async def get_withdrawal_status(
        self, withdrawal_id: str
    ) -> WithdrawalStatus:
        return await self.get_withdrawal(withdrawal_id=withdrawal_id).status


    async def create_cheque(
        self,
        *,
        currency: str,
        total: int,
        users: int,
        description: Optional[str] = None,
        password: Optional[str] = None,
        send_notifications: Optional[bool] = None,
        captcha_enabled: Optional[bool] = None,
        tg_resources: Optional[List[str]] = None,
        ref_program_percents: Optional[int] = None,
        disabled_languages: Optional[List[str]] = None,
        for_premium: Optional[bool] = None,
        for_new_users_only: Optional[bool] = None,
        linked_wallet: Optional[bool] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Cheque:
        """
        Create a multi-cheque that can be claimed by multiple users.

        Args:
            currency: Currency code.
            total: Total amount across all users.
            users: Number of users who can claim.
            description: Optional public description.
            password: Optional password to protect the cheque.
            send_notifications: Whether to notify via Telegram channels.
            captcha_enabled: Whether to protect by captcha.
            tg_resources: Telegram resources for promotion.
            ref_program_percents: Referral program percent.
            disabled_languages: List of disabled interface languages.
            for_premium: Only for Telegram Premium users.
            for_new_users_only: Only for new xRocket users.
            linked_wallet: Link to a wallet (if supported).
            extra: Optional additional official fields.

        Returns:
            Cheque model.
        """
        payload: Dict[str, Any] = {
            "currency": currency,
            "total": total,
            "users": users,
        }
        if description is not None:
            payload["description"] = description
        if password is not None:
            payload["password"] = password
        if send_notifications is not None:
            payload["sendNotifications"] = send_notifications
        if captcha_enabled is not None:
            payload["captchaEnabled"] = captcha_enabled
        if tg_resources is not None:
            payload["tgResources"] = tg_resources
        if ref_program_percents is not None:
            payload["refProgramPercents"] = ref_program_percents
        if disabled_languages is not None:
            payload["disabledLanguages"] = disabled_languages
        if for_premium is not None:
            payload["forPremium"] = for_premium
        if for_new_users_only is not None:
            payload["forNewUsersOnly"] = for_new_users_only
        if linked_wallet is not None:
            payload["linkedWallet"] = linked_wallet
        if extra:
            payload.update(extra)

        r = await self._request("POST", "multi-cheques", json=payload)
        return Cheque.from_api(r["data"])

    async def get_cheque(self, cheque_id: int) -> Cheque:
        """
        Fetch a single cheque by its ID.
        """
        r = await self._request("GET", f"multi-cheques/{cheque_id}")
        return Cheque.from_api(r["data"])

    async def edit_cheque(
        self,
        cheque_id: int,
        *,
        description: Optional[str] = None,
        password: Optional[str] = None,
        send_notifications: Optional[bool] = None,
        captcha_enabled: Optional[bool] = None,
        tg_resources: Optional[List[str]] = None,
        ref_program_percents: Optional[int] = None,
        disabled_languages: Optional[List[str]] = None,
        for_premium: Optional[bool] = None,
        for_new_users_only: Optional[bool] = None,
        linked_wallet: Optional[bool] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Cheque:
        """
        Update editable fields of a cheque.

        Only fields that are provided will be sent to the API.
        """
        payload: Dict[str, Any] = {}
        if description is not None:
            payload["description"] = description
        if password is not None:
            payload["password"] = password
        if send_notifications is not None:
            payload["sendNotifications"] = send_notifications
        if captcha_enabled is not None:
            payload["captchaEnabled"] = captcha_enabled
        if tg_resources is not None:
            payload["tgResources"] = tg_resources
        if ref_program_percents is not None:
            payload["refProgramPercents"] = ref_program_percents
        if disabled_languages is not None:
            payload["disabledLanguages"] = disabled_languages
        if for_premium is not None:
            payload["forPremium"] = for_premium
        if for_new_users_only is not None:
            payload["forNewUsersOnly"] = for_new_users_only
        if linked_wallet is not None:
            payload["linkedWallet"] = linked_wallet
        if extra:
            payload.update(extra)

        r = await self._request("PUT", f"multi-cheques/{cheque_id}", json=payload)
        return Cheque.from_api(r["data"])

    async def delete_cheque(self, cheque_id: int) -> None:
        """
        Delete a cheque by ID.
        """
        await self._request("DELETE", f"multi-cheques/{cheque_id}")

    async def list_cheques(self, *, limit: int = 100, offset: int = 0) -> List[Cheque]:
        """
        List cheques with pagination.
        """
        r = await self._request("GET", "multi-cheques", params={"limit": limit, "offset": offset})
        return [Cheque.from_api(c) for c in r["data"].get("results", [])]

    async def iter_cheques(self, *, page_size: int = 100, start_offset: int = 0) -> AsyncIterator[Cheque]:
        """
        Iterate over all cheques as an async generator.
        """
        offset = start_offset
        while True:
            batch = await self.list_cheques(limit=page_size, offset=offset)
            if not batch:
                return
            for c in batch:
                yield c
            offset += len(batch)

    # =========================
    # Public API: Telegram Invoices
    # =========================

    async def create_invoice(
        self,
        *,
        amount: int,
        currency: str,
        description: Optional[str] = None,
        hidden_message: Optional[str] = None,
        payload: Optional[str] = None,
        callback_url: Optional[str] = None,
        expired_in: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Invoice:
        """
        Create a Telegram invoice.

        Args:
            amount: Amount to charge (integer, per API docs).
            currency: Currency code.
            description: Optional description text.
            hidden_message: Optional hidden message shown after payment.
            payload: Optional opaque payload string returned in callback.
            callback_url: Optional webhook URL for payment updates.
            expired_in: Optional TTL in seconds.
            extra: Optional additional official fields.

        Returns:
            Invoice model.
        """
        payload_dict: Dict[str, Any] = {"amount": amount, "currency": currency}
        if description is not None:
            payload_dict["description"] = description
        if hidden_message is not None:
            payload_dict["hiddenMessage"] = hidden_message
        if payload is not None:
            payload_dict["payload"] = payload
        if callback_url is not None:
            payload_dict["callbackUrl"] = callback_url
        if expired_in is not None:
            payload_dict["expiredIn"] = expired_in
        if extra:
            payload_dict.update(extra)

        r = await self._request("POST", "tg-invoices", json=payload_dict)
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

    async def available_currencies(self) -> List[Currency]:
        """
        Get the list of available currencies and their operational constraints.

        Notes:
            Documentation indicates this endpoint is public; we request it without auth header.
        """
        r = await self._request("GET", "currencies/available", require_auth_header=False)
        return [Currency.from_api(c) for c in r["data"].get("results", [])]
