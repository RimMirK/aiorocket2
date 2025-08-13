from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

from .enums import *

# __all__ = [
#     'Info',
#     'Balance',
#     'Transfer',
#     "Withdrawal",
#     "Cheque",
#     "Invoice",
#     "Currency",
# ]

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
            balance=j.get('balance', 0.0)
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
            address=j.get('address'),
            currency=j.get('currency'),
            amount=j.get('amount', 0),
            withdrawal_id=j.get('withdrawalId'),
            status=WithdrawalStatus(j.get('status') or "UNKNOWN"),
            comment=j.get('comment'),
            tx_hash=j.get('txHash'),
            tx_link=j.get('txLink'),
        )

@dataclass(slots=True)
class WithdrawalCoin:
    code: str
    """Crypto code"""
    min_withdrawal: float
    """Minimal amount for withdrawals"""
    fees: List["WithdrawalCoinFees"]
    
    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "WithdrawalCoin":
        """
        Build WithdrawalCoin from API JSON object.
        """
        return cls(
            code=j.get('code'),
            min_withdrawal=j.get('minWithdrawal'),
            fees=[WithdrawalCoinFees.from_api(fee) for fee in j.get("fees", [])]
        )

@dataclass(slots=True)
class WithdrawalCoinFees:
    network_code: Network
    """Network code for withdraw"""
    fee: float
    """Fee amount"""
    currency: str
    """Withdraw fee currency"""
    
    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "WithdrawalCoinFees":
        """
        Build WithdrawalCoinFees from API JSON object.
        """
        return cls(
            network_code=Network(j.get('networkCode') or 'UNKNOWN'),
            fee=j.get('feeWithdraw', {}).get("fee"),
            currency=j.get('feeWithdraw', {}).get('currency')
        )

@dataclass(slots=True)
class Cheque:
    """
    Represents a multi-cheque entity returned by the xRocket Pay API.
    """
    id: int
    """Cheque ID"""
    currency: str
    total: int
    """Total amount of cheque (this amount is charged from balance)"""
    per_user: int
    """Amount of cheque per user"""
    users: int
    """Number of users that can activate your cheque"""
    password: str
    """Cheque password"""
    description: str
    """Cheque description"""
    send_notifications: bool
    """send notifications about cheque activation to application cheque webhook or not"""
    ref_program_percents: int
    """percentage of cheque that rewarded for referral program"""
    ref_reward_per_user: float
    """amount of referral user reward"""
    captcha_enabled: bool
    """enable / disable cheque captcha"""
    state: ChequeState
    link: str
    disabled_languages: List[str]
    """Disable languages"""
    enabled_countries: List[Country]
    """Enabled countries"""
    for_premium: bool
    """Only users with Telegram Premium can activate this cheque"""
    for_new_users_only: bool
    """Only new users can activate this cheque"""
    linked_wallet: bool
    """Only users with connected wallets can activate this cheque"""
    tg_resources: List[TgResource]
    activations: int
    """How many times cheque is activate"""
    ref_rewards: int
    """How many times referral reward is payed"""


    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "Cheque":
        """
        Build Cheque from API JSON object.
        """
        return cls(
            id=j.get("id"),
            currency=j.get("currency"),
            total=j.get("total", 0),
            per_user=j.get("perUser", 0),
            users=j.get("users", 0),
            password=j.get("password"),
            description=j.get("description"),
            send_notifications=j.get("sendNotifications", False),
            captcha_enabled=j.get("captchaEnabled", False),
            ref_program_percents=j.get("refProgramPercents", 0),
            ref_reward_per_user=j.get("refRewardPerUser", 0),
            state=ChequeState(j.get('state') or "UNKNOWN"),
            link=j.get("link", ""),
            disabled_languages=j.get("disabledLanguages", []),
            enabled_countries=[Country(country) for country in j.get('enabledCountries', [])],
            for_premium=bool(j.get("forPremium", False)),
            for_new_users_only=bool(j.get("forNewUsersOnly", False)),
            linked_wallet=bool(j.get("linkedWallet", False)),
            tg_resources=[TgResource.from_api(resourse) for resourse in j.get('resourses', [])],
            activations=j.get("activations", 0),
            ref_rewards=j.get("refRewards", 0),
        )


@dataclass(slots=True)
class TgResource:
    """
    Represents a TgResourse entity returned by the xRocket Pay API.
    """
    telegram_id: int
    name: str
    username: str

    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "TgResource":
        """
        Build Cheque from API JSON object.
        """
        return cls(
            telegram_id=j.get("telegramId"),
            name=j.get("name"),
            username=j.get("username")
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
