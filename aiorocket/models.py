from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

from .enums import *

__all__ = [
    'Info',
    'Balance',
    'Transfer',
    "Withdrawal",
    "Cheque",
    "Invoice",
    "Currency"
]

@dataclass(slots=True)
class Info:
    """
    Represents a info entity returned by the xRocket Pay API.
    """
    name: str
    """Name of current app"""
    fee_percents: float
    """Fee for incoming transactions"""
    balances: List["Balance"]

    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "Info":
        """
        Build Info from API JSON object.
        """
        return cls(
            name=j.get('name'),
            fee_percents=j.get('feePercents', 1.5),
            balances=[Balance.from_api(balance) for balance in j.get('balances', [])]
        )

@dataclass(slots=True)
class Balance:
    
    """
    Represents a balance entity returned by the xRocket Pay API.
    """
    currency: str
    balance: float
    
    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "Balance":
        """
        Build Info from API JSON object.
        """
        return cls(
            currency=j.get('currency'),
            Balance=j.get('balance', 0.0)
        )

@dataclass(slots=True)
class Transfer:
    """
    Represents a transfer entity returned by the xRocket Pay API.
    """
    id: int
    """Transfer ID"""
    tg_user_id: int
    """"""
    currency: str
    """Currency code"""
    amount: float
    """Transfer amount. 9 decimal places, others cut off"""
    description: str
    """Transfer description"""

    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "Transfer":
        """
        Build Transfer from API JSON object.
        """
        return cls(
            id=j.get('id'),
            tg_user_id=j.get("tgUserId"),
            currency=j.get('currency'),
            amount=j.get("amount", 0.0),
            description=j.get('description')
        )

@dataclass(slots=True)
class Withdrawal:
    network: Network
    """Network code."""
    address: str
    """Withdrawal address"""
    currency: str
    """Currency code"""
    amount: float
    """Withdrawal amount. 9 decimal places, others cut off"""
    withdrawal_id: str
    """Unique withdrawal ID in your system to prevent double spends"""
    status: WithdrawalStatus
    """Withdrawal status"""
    comment: str
    """Withdrawal comment"""
    tx_hash: str
    """Withdrawal TX hash. Provided only after withdrawal. """
    tx_link: str
    """Withdrawal TX link. Provided only after withdrawal"""
    
    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "Withdrawal":
        """
        Build Withdrawal from API JSON object.
        """
        return cls(
            network=Network(j.get('network') or "UNKNOWN"),
            currency=j.get('currency'),
            amount=j.get('amount', 0),
            withdrawal_id=j.get('withdrawalId'),
            status=WithdrawalStatus(j.get('status') or "UNKNOWN"),
            comment=j.get('comment'),
            tx_hash=j.get('txHash'),
            tx_link=j.get('txLink'),
        )

@dataclass(slots=True)
class Cheque:
    """
    Represents a multi-cheque entity returned by the xRocket Pay API.
    """
    id: int
    currency: str
    total: int
    users: int
    password: Optional[str]
    description: Optional[str]
    notifications: bool
    captcha: bool
    telegram_resources: List[str]
    ref_percents: int
    state: str
    link: str
    activations: int
    ref_rewards: int
    disabled_langs: List[str]
    for_premium: bool
    for_new_users: bool
    linked_wallet: bool
    per_user: float = field(init=False)

    def __post_init__(self) -> None:
        self.per_user = (self.total / self.users) if self.users else 0.0

    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "Cheque":
        """
        Build Cheque from API JSON object.
        """
        return cls(
            id=j.get("id"),
            currency=j.get("currency"),
            total=j.get("total"),
            users=j.get("users"),
            password=j.get("password"),
            description=j.get("description"),
            notifications=j.get("sendNotifications", False),
            captcha=j.get("captchaEnabled", False),
            telegram_resources=list(j.get("tgResources", []) or []),
            ref_percents=j.get("refProgramPercents", 0),
            state=j.get("state", ""),
            link=j.get("link", ""),
            activations=j.get("activations", 0),
            ref_rewards=j.get("refRewards", 0),
            disabled_langs=list(j.get("disabledLanguages", []) or []),
            for_premium=j.get("forPremium", False),
            for_new_users=j.get("forNewUsersOnly", False),
            linked_wallet=j.get("linkedWallet", False),
        )

@dataclass(slots=True)
class Invoice:
    """
    Represents a Telegram invoice entity returned by the xRocket Pay API.
    """
    id: int
    amount: int
    total_payments: int
    payments_left: int
    description: Optional[str]
    hidden_message: Optional[str]
    payload: Optional[str]
    callback_url: Optional[str]
    currency: str
    created: str
    paid: Optional[str]
    status: str
    expired_in: int
    link: str
    payments: List[Dict[str, Any]]

    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "Invoice":
        """
        Build Invoice from API JSON object.
        """
        return cls(
            id=j.get("id"),
            amount=j.get("amount"),
            total_payments=j.get("totalActivations", 0),
            payments_left=j.get("activationsLeft", 0),
            description=j.get("description"),
            hidden_message=j.get("hiddenMessage"),
            payload=j.get("payload"),
            callback_url=j.get("callbackUrl"),
            currency=j.get("currency"),
            created=j.get("created"),
            paid=j.get("paid"),
            status=j.get("status", ""),
            expired_in=j.get("expiredIn", 0),
            link=j.get("link", ""),
            payments=list(j.get("payments", []) or []),
        )

@dataclass(slots=True)
class Currency:
    """
    Represents a currency capabilities descriptor from /currencies/available.
    """
    currency: str
    ticker: str
    min_transfer: float
    min_cheque: float
    min_invoice: float
    min_withdraw: float
    withdraw_fee: float

    def __str__(self) -> str:
        return self.currency

    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "Currency":
        """
        Build Currency from API JSON object.
        """
        return cls(
            currency=j.get("currency"),
            ticker=j.get("name"),
            min_transfer=j.get("minTransfer"),
            min_cheque=j.get("minCheque"),
            min_invoice=j.get("minInvoice"),
            min_withdraw=j.get("minWithdraw"),
            withdraw_fee=j.get("feeWithdraw"),
        )
