from __future__ import annotations

from dataclasses import dataclass, is_dataclass, asdict
from enum import Enum
from typing import Any, List, Mapping, Self
from datetime import datetime, timezone


from .enums import *

__all__ = [
    'Info',
    'Balance',
    'Transfer',
    "Withdrawal",
    'WithdrawalCoin',
    'WithdrawalCoinFees',
    "Cheque",
    "TgResource",
    "PaginatedCheque",
    "Invoice",
    "PaginatedInvoice",
    "WithdrawalFee",
    "Currency",
]

def to_dict(obj, keep_enums=False):
    if is_dataclass(obj):
        return {k: to_dict(v, keep_enums=keep_enums) for k, v in asdict(obj).items()}
    elif isinstance(obj, Enum):
        return obj if keep_enums else obj.value
    elif isinstance(obj, list):
        return [to_dict(x, keep_enums=keep_enums) for x in obj]
    elif isinstance(obj, dict):
        return {k: to_dict(v, keep_enums=keep_enums) for k, v in obj.items()}
    else:
        return obj

class Base:
    def as_dict(self, keep_enums=False):
        return to_dict(self, keep_enums=keep_enums)
    
    def __iter__(self):
        return iter(self.as_dict(keep_enums=True).items())
    
    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "Self":
        raise NotImplementedError

@dataclass(slots=True)
class Info(Base):
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
class Balance(Base):
    
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
class Transfer(Base):
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
class Withdrawal(Base):
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
class WithdrawalCoin(Base):
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
class WithdrawalCoinFees(Base):
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
class Cheque(Base):
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
class TgResource(Base):
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
class PaginatedCheque(Base):
    total: int
    """Total times"""
    limit: int
    offset: int
    results: List[Cheque]
    
    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "PaginatedCheque":
        """
        Build PaginatedCheque from API JSON object.
        """
        return cls(
            total=j.get('total', 0),
            limit=j.get('limit', 0),
            offset=j.get('offset', 0),
            results=[Cheque.from_api(cheque) for cheque in j.get('results', [])]
        )

@dataclass(slots=True)
class DateTimeStr(str, Base):
    
    def __init__(self, value):
        super(str, self).__init__()
        self.value = value
        self.raw = value
    
    def __str__(self):
        return str(self.datetime)
    
    @property
    def datetime(self) -> datetime:
        if self.value:
            return datetime.fromisoformat(self.value.replace("Z", "+00:00"))
        return datetime.fromtimestamp(0, timezone.utc)
    
    @property
    def timestamp(self) -> float:
        if self.value:
            return self.datetime.timestamp()
        return 0
    
@dataclass(slots=True)
class Invoice(Base):
    """
    Represents a Invoice entity returned by the xRocket Pay API.
    """
    id: int
    """Invoice ID"""
    amount: float
    """Amount of invoice"""
    min_payment: float
    """Min payment of invoice"""
    total_activations: int
    """Total activations of invoice"""
    activations_left: int
    """Activations left of invoice"""
    description: str
    """Invoice description"""
    hidden_message: str
    """Message that will be displayed after invoice payment"""
    payload: str
    """Any data that is attached to invoice"""
    callback_url: str
    """url that will be set for Return button after invoice is paid"""
    comments_enabled: bool
    """Allow comments for invoice"""
    currency: str
    created: DateTimeStr
    """(date-time) When invoice was created"""
    paid: DateTimeStr
    """(date-time) When invoice was paid"""
    status: InvoiceStatus
    expired_in: int
    """Invoice expire time in seconds, max 1 day, 0 - none expired"""
    link: str

    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "Invoice":
        """
        Build Invoice from API JSON object.
        """
        return cls(
            id=j.get("id"),
            amount=j.get("amount", 0),
            min_payment=j.get("minPayment", 0),
            total_activations=j.get("totalActivations", 0),
            activations_left=j.get("activationsLeft", 0),
            description=j.get("description"),
            hidden_message=j.get("hiddenMessage"),
            payload=j.get("payload"),
            callback_url=j.get("callbackUrl"),
            comments_enabled=j.get("commentsEnabled", False),
            currency=j.get("currency"),
            created=DateTimeStr(j.get("created")),
            paid=DateTimeStr(j.get("paid")),
            status=InvoiceStatus(j.get("status") or "UNKNOWN"),
            expired_in=j.get("expiredIn", 0),
            link=j.get("link")
        )

@dataclass(slots=True)
class PaginatedInvoice(Base):
    total: int
    """Total times"""
    limit: int
    offset: int
    results: List[Invoice]
    
    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "PaginatedInvoice":
        """
        Build PaginatedInvoice from API JSON object.
        """
        return cls(
            total=j.get('total', 0),
            limit=j.get('limit', 0),
            offset=j.get('offset', 0),
            results=[Invoice.from_api(cheque) for cheque in j.get('results', [])]
        )
    
@dataclass(slots=True)
class WithdrawalFee(Base):
    """
    Represents a WithdrawalFee entity returned by the xRocket Pay API.
    """
    currency: str
    """ID of main currency for token"""
    networks: List[WithdrawalCoinFees]

    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "WithdrawalFee":
        """
        Build WithdrawalFee from API JSON object.
        """
        return cls(
            currency=j.get('currency'),
            networks=[
                WithdrawalCoinFees(
                    network_code=Network(network.get("networkCode") or "UNKNOWN"),
                    fee=network.get("feeWithdraw", {}).get("fee", 0),
                    currency=network.get("feeWithdraw", {}).get("currency"),
                ) for network in j.get('networks', [])
            ]
        )

@dataclass(slots=True)
class Currency(Base):
    """
    Represents a Currency entity returned by the xRocket Pay API.
    """
    currency: str
    """ID of currency, use in Rocket Pay Api"""
    name: str
    """Name of currency"""
    min_transfer: float
    """Minimal amount for transfer"""
    min_cheque: float
    """Minimal amount for cheque"""
    min_invoice: float
    """Minimal amount for invoice"""
    min_withdraw: float
    """Minimal amount for withdrawals"""
    withdraw_fee: WithdrawalFee

    @classmethod
    def from_api(cls, j: Mapping[str, Any]) -> "Currency":
        """
        Build Currency from API JSON object.
        """
        return cls(
            currency=j.get("currency"),
            name=j.get("name"),
            min_transfer=j.get("minTransfer", 0),
            min_cheque=j.get("minCheque", 0),
            min_invoice=j.get("minInvoice", 0),
            min_withdraw=j.get("minWithdraw", 0),
            withdraw_fee=WithdrawalFee.from_api(j.get("feeWithdraw")),
        )
