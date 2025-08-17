---
sidebar_position: 3
title: Models (dataclases)
---

---


## Base Object

```python
class Base()
```

Base class for all models

---

### `as_dict`

```python
def as_dict(keep_enums=False, keep_datetime=False) -> dict
```

**Note:**
- To export data use method `.as_dict()`.
- To just convert data to a dict use built-in function `dict()`


### `from_api`

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> Self
```

Build model from api data



## `Info`

```python
@dataclass
class Info(Base)
```

Represents a info entity returned by the xRocket Pay API.
- `name`: Name of current app
- `fee_percents`: Fee for incoming transactions

## `Balance`

```python
@dataclass
class Balance(Base)
```

Represents a balance entity returned by the xRocket Pay API.

## `Transfer`

```python
@dataclass
class Transfer(Base)
```

Represents a transfer entity returned by the xRocket Pay API.
- `id`: Transfer ID
- `tg_user_id`: 
- `currency`: Currency code
- `amount`: Transfer amount. 9 decimal places, others cut off
- `description`: Transfer description

## `Withdrawal`

```python
@dataclass
class Withdrawal(Base)
```

Represents a Withdrawal entity returned by the xRocket Pay API.
- `network`: [`Network`](enums#Network) Network code.
- `address`: Withdrawal address
- `currency`: Currency code
- `amount`: Withdrawal amount. 9 decimal places, others cut off
- `withdrawal_id`: Unique withdrawal ID in your system to prevent double spends
- `status`: Withdrawal status
- `comment`: Withdrawal comment
- `tx_hash`: Withdrawal TX hash. Provided only after withdrawal.
- `tx_link`: Withdrawal TX link. Provided only after withdrawal

## `WithdrawalCoin`

```python
@dataclass
class WithdrawalCoin(Base)
```

Represents a WithdrawalCoin entity returned by the xRocket Pay API.
- `code`: Crypto code
- `min_withdrawal`: Minimal amount for withdrawals

## `WithdrawalCoinFees`

```python
@dataclass
class WithdrawalCoinFees(Base)
```

Represents a WithdrawalCoinFees entity returned by the xRocket Pay API.
- `network_code`: [`Network`](enums#Network) Network code for withdraw
- `fee`: Fee amount
- `currency`: Withdraw fee currency

## `Cheque`

```python
@dataclass
class Cheque(Base)
```

Represents a multi-cheque entity returned by the xRocket Pay API.
- `id`: Cheque ID
- `total`: Total amount of cheque (this amount is charged from balance)
- `per_user`: Amount of cheque per user
- `users`: Number of users that can activate your cheque
- `password`: Cheque password
- `description`: Cheque description
- `send_notifications`: send notifications about cheque activation to application cheque webhook or not
- `ref_program_percents`: percentage of cheque that rewarded for referral program
- `ref_reward_per_user`: amount of referral user reward
- `captcha_enabled`: enable / disable cheque captcha
- `disabled_languages`: Disable languages
- `enabled_countries`: Enabled countries
- `for_premium`: Only users with Telegram Premium can activate this cheque
- `for_new_users_only`: Only new users can activate this cheque
- `linked_wallet`: Only users with connected wallets can activate this cheque
- `activations`: How many times cheque is activate
- `ref_rewards`: How many times referral reward is payed

## `TgResource`

```python
@dataclass
class TgResource(Base)
```

Represents a TgResourse entity returned by the xRocket Pay API.

## `PaginatedCheque`

```python
@dataclass
class PaginatedCheque(Base)
```

Represents a PaginatedCheque entity returned by the xRocket Pay API.
- `total`: Total times

## `DateTimeStr`

```python
@dataclass
class DateTimeStr(str, Base)
```

Time object, to comfortable get time from the api

## `Invoice`

```python
@dataclass
class Invoice(Base)
```

Represents a Invoice entity returned by the xRocket Pay API.
- `id`: Invoice ID
- `amount`: Amount of invoice
- `min_payment`: Min payment of invoice
- `total_activations`: Total activations of invoice
- `activations_left`: Activations left of invoice
- `description`: Invoice description
- `hidden_message`: Message that will be displayed after invoice payment
- `payload`: Any data that is attached to invoice
- `callback_url`: url that will be set for Return button after invoice is paid
- `comments_enabled`: Allow comments for invoice
- `created`: (date-time) When invoice was created
- `paid`: (date-time) When invoice was paid
- `expired_in`: Invoice expire time in seconds, max 1 day, 0 - none expired

## `PaginatedInvoice`

```python
@dataclass
class PaginatedInvoice(Base)
```

Represents a PaginatedInvoice entity returned by the xRocket Pay API.
- `total`: Total times

## `WithdrawalFee`

```python
@dataclass
class WithdrawalFee(Base)
```

Represents a WithdrawalFee entity returned by the xRocket Pay API.
- `currency`: ID of main currency for token

## `Currency`

```python
@dataclass
class Currency(Base)
```

Represents a Currency entity returned by the xRocket Pay API.
- `currency`: ID of currency, use in Rocket Pay Api
- `name`: Name of currency
- `min_transfer`: Minimal amount for transfer
- `min_cheque`: Minimal amount for cheque
- `min_invoice`: Minimal amount for invoice
- `min_withdraw`: Minimal amount for withdrawals
