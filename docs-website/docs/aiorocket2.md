<a id="aiorocket2"></a>

# aiorocket2

aiorocket2 — idiomatic async Python client for the xRocket Pay API.

<a id="aiorocket2.client"></a>

# aiorocket2.client

TODO

<a id="aiorocket2.client.xRocketClient"></a>

## xRocketClient Objects

```python
class xRocketClient(Tags)
```

Asynchronous client for the xRocket Pay API.

<a id="aiorocket2.client.xRocketClient.__init__"></a>

#### \_\_init\_\_

```python
def __init__(api_key: str,
             *,
             testnet: bool = False,
             base_url: Optional[str] = None,
             session: Optional[aiohttp.ClientSession] = None,
             timeout: float = DEFAULT_TIMEOUT,
             retries: int = DEFAULT_RETRIES,
             backoff_base: float = DEFAULT_BACKOFF_BASE,
             user_agent: str = DEFAULT_USER_AGENT) -> None
```

Initialize the client.

**Arguments**:

- `api_key` - Your xRocket Pay API key.
- `testnet` - If True, use the staging/test environment.
- `base_url` - Optional override for the base API URL.
- `session` - Optional aiohttp session to reuse.
- `timeout` - aiohttp total timeout (seconds).
- `retries` - Number of retries for network/5xx errors.
- `backoff_base` - Base delay for exponential backoff (seconds).
- `user_agent` - Custom User-Agent header value.

<a id="aiorocket2.client.xRocketClient.aclose"></a>

#### aclose

```python
async def aclose() -> None
```

Close the underlying aiohttp session if it was created by this client.

<a id="aiorocket2.client_api"></a>

# aiorocket2.client\_api

<a id="aiorocket2.client_api.ClientAPI"></a>

## ClientAPI Objects

```python
class ClientAPI(xRocketClient)
```

Aggregated xRocketClient with all tag methods

<a id="aiorocket2.constants"></a>

# aiorocket2.constants

Constants used by the aiorocket2 package.

<a id="aiorocket2.constants.DEFAULT_TIMEOUT"></a>

#### DEFAULT\_TIMEOUT

seconds (aiohttp total timeout)

<a id="aiorocket2.constants.DEFAULT_RETRIES"></a>

#### DEFAULT\_RETRIES

network/5xx retries

<a id="aiorocket2.constants.DEFAULT_BACKOFF_BASE"></a>

#### DEFAULT\_BACKOFF\_BASE

seconds

<a id="aiorocket2.enums"></a>

# aiorocket2.enums

Enums used by aiorocket2

<a id="aiorocket2.enums.WithdrawalStatus"></a>

## WithdrawalStatus Objects

```python
class WithdrawalStatus(Base)
```

<a id="aiorocket2.enums.WithdrawalStatus.UNKNOWN"></a>

#### UNKNOWN

Returned when xRocket API does not sent value

<a id="aiorocket2.enums.Network"></a>

## Network Objects

```python
class Network(Base)
```

<a id="aiorocket2.enums.Network.UNKNOWN"></a>

#### UNKNOWN

Returned when xRocket API does not sent value

<a id="aiorocket2.enums.Country"></a>

## Country Objects

```python
class Country(Base)
```

<a id="aiorocket2.enums.Country.UNKNOWN"></a>

#### UNKNOWN

Returned when xRocket API does not sent value

<a id="aiorocket2.enums.ChequeState"></a>

## ChequeState Objects

```python
class ChequeState(Base)
```

Active - cheque created and has unclaimed activations.
Completed - cheque totally activated.

<a id="aiorocket2.enums.ChequeState.ACTIVE"></a>

#### ACTIVE

cheque created and has unclaimed activations.

<a id="aiorocket2.enums.ChequeState.COMPLETED"></a>

#### COMPLETED

cheque totally activated.

<a id="aiorocket2.enums.ChequeState.UNKNOWN"></a>

#### UNKNOWN

Returned when xRocket API does not sent value

<a id="aiorocket2.enums.InvoiceStatus"></a>

## InvoiceStatus Objects

```python
class InvoiceStatus(Base)
```

<a id="aiorocket2.enums.InvoiceStatus.UNKNOWN"></a>

#### UNKNOWN

Returned when xRocket API does not sent value

<a id="aiorocket2.enums.Status"></a>

## Status Objects

```python
class Status(Base)
```

<a id="aiorocket2.enums.Status.UNKNOWN"></a>

#### UNKNOWN

Returned when xRocket API does not sent value

<a id="aiorocket2.exceptions"></a>

# aiorocket2.exceptions

Exceptions used by aiorocket2

<a id="aiorocket2.exceptions.xRocketAPIError"></a>

## xRocketAPIError Objects

```python
class xRocketAPIError(Exception)
```

High-level API error that always carries the raw API payload and (if available) HTTP status.

**Attributes**:

- `message` - Human-readable error message.
- `payload` - Raw JSON payload returned by the API.
- `status` - HTTP status code (if known).

<a id="aiorocket2.models"></a>

# aiorocket2.models

Modules (dataclases) used by aiorocket2

<a id="aiorocket2.models.to_dict"></a>

#### to\_dict

```python
def to_dict(obj, keep_enums=False, keep_datetime=False) -> dict
```

Recursively converts an object to a dictionary suitable for JSON serialization.

Supports:
- dataclass: recursively converts all fields.
- Enum: returns the enum value if keep_enums=False, otherwise returns the Enum object.
- list: recursively converts all elements.
- dict: recursively converts all values.
- datetime: returns ISO-formatted string if keep_datetime=False, otherwise returns the datetime object.

**Arguments**:

- `obj` _Any_ - Any object to convert.
- `keep_enums` _bool_ - If True, keeps Enum objects, otherwise returns their values.
- `keep_datetime` _bool_ - If True, keeps datetime objects, otherwise returns ISO string.
  

**Returns**:

- `dict` - recursively converted object.

<a id="aiorocket2.models.Base"></a>

## Base Objects

```python
class Base()
```

Base class for all models

<a id="aiorocket2.models.Base.as_dict"></a>

#### as\_dict

```python
def as_dict(keep_enums=False, keep_datetime=False) -> dict
```

### Note:
- To export data use method `.as_dict()`.
- To just convert data to a dict use built-in function `dict()`

<a id="aiorocket2.models.Base.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any])
```

Build model from api data

<a id="aiorocket2.models.Info"></a>

## Info Objects

```python
@dataclass
class Info(Base)
```

Represents a info entity returned by the xRocket Pay API.

<a id="aiorocket2.models.Info.name"></a>

#### name

Name of current app

<a id="aiorocket2.models.Info.fee_percents"></a>

#### fee\_percents

Fee for incoming transactions

<a id="aiorocket2.models.Info.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "Info"
```

Build Info from API JSON object.

<a id="aiorocket2.models.Balance"></a>

## Balance Objects

```python
@dataclass
class Balance(Base)
```

Represents a balance entity returned by the xRocket Pay API.

<a id="aiorocket2.models.Balance.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "Balance"
```

Build Info from API JSON object.

<a id="aiorocket2.models.Transfer"></a>

## Transfer Objects

```python
@dataclass
class Transfer(Base)
```

Represents a transfer entity returned by the xRocket Pay API.

<a id="aiorocket2.models.Transfer.id"></a>

#### id

Transfer ID

<a id="aiorocket2.models.Transfer.tg_user_id"></a>

#### tg\_user\_id



<a id="aiorocket2.models.Transfer.currency"></a>

#### currency

Currency code

<a id="aiorocket2.models.Transfer.amount"></a>

#### amount

Transfer amount. 9 decimal places, others cut off

<a id="aiorocket2.models.Transfer.description"></a>

#### description

Transfer description

<a id="aiorocket2.models.Transfer.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "Transfer"
```

Build Transfer from API JSON object.

<a id="aiorocket2.models.Withdrawal"></a>

## Withdrawal Objects

```python
@dataclass
class Withdrawal(Base)
```

Represents a Withdrawal entity returned by the xRocket Pay API.

<a id="aiorocket2.models.Withdrawal.network"></a>

#### network

Network code.

<a id="aiorocket2.models.Withdrawal.address"></a>

#### address

Withdrawal address

<a id="aiorocket2.models.Withdrawal.currency"></a>

#### currency

Currency code

<a id="aiorocket2.models.Withdrawal.amount"></a>

#### amount

Withdrawal amount. 9 decimal places, others cut off

<a id="aiorocket2.models.Withdrawal.withdrawal_id"></a>

#### withdrawal\_id

Unique withdrawal ID in your system to prevent double spends

<a id="aiorocket2.models.Withdrawal.status"></a>

#### status

Withdrawal status

<a id="aiorocket2.models.Withdrawal.comment"></a>

#### comment

Withdrawal comment

<a id="aiorocket2.models.Withdrawal.tx_hash"></a>

#### tx\_hash

Withdrawal TX hash. Provided only after withdrawal.

<a id="aiorocket2.models.Withdrawal.tx_link"></a>

#### tx\_link

Withdrawal TX link. Provided only after withdrawal

<a id="aiorocket2.models.Withdrawal.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "Withdrawal"
```

Build Withdrawal from API JSON object.

<a id="aiorocket2.models.WithdrawalCoin"></a>

## WithdrawalCoin Objects

```python
@dataclass
class WithdrawalCoin(Base)
```

Represents a WithdrawalCoin entity returned by the xRocket Pay API.

<a id="aiorocket2.models.WithdrawalCoin.code"></a>

#### code

Crypto code

<a id="aiorocket2.models.WithdrawalCoin.min_withdrawal"></a>

#### min\_withdrawal

Minimal amount for withdrawals

<a id="aiorocket2.models.WithdrawalCoin.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "WithdrawalCoin"
```

Build WithdrawalCoin from API JSON object.

<a id="aiorocket2.models.WithdrawalCoinFees"></a>

## WithdrawalCoinFees Objects

```python
@dataclass
class WithdrawalCoinFees(Base)
```

Represents a WithdrawalCoinFees entity returned by the xRocket Pay API.

<a id="aiorocket2.models.WithdrawalCoinFees.network_code"></a>

#### network\_code

Network code for withdraw

<a id="aiorocket2.models.WithdrawalCoinFees.fee"></a>

#### fee

Fee amount

<a id="aiorocket2.models.WithdrawalCoinFees.currency"></a>

#### currency

Withdraw fee currency

<a id="aiorocket2.models.WithdrawalCoinFees.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "WithdrawalCoinFees"
```

Build WithdrawalCoinFees from API JSON object.

<a id="aiorocket2.models.Cheque"></a>

## Cheque Objects

```python
@dataclass
class Cheque(Base)
```

Represents a multi-cheque entity returned by the xRocket Pay API.

<a id="aiorocket2.models.Cheque.id"></a>

#### id

Cheque ID

<a id="aiorocket2.models.Cheque.total"></a>

#### total

Total amount of cheque (this amount is charged from balance)

<a id="aiorocket2.models.Cheque.per_user"></a>

#### per\_user

Amount of cheque per user

<a id="aiorocket2.models.Cheque.users"></a>

#### users

Number of users that can activate your cheque

<a id="aiorocket2.models.Cheque.password"></a>

#### password

Cheque password

<a id="aiorocket2.models.Cheque.description"></a>

#### description

Cheque description

<a id="aiorocket2.models.Cheque.send_notifications"></a>

#### send\_notifications

send notifications about cheque activation to application cheque webhook or not

<a id="aiorocket2.models.Cheque.ref_program_percents"></a>

#### ref\_program\_percents

percentage of cheque that rewarded for referral program

<a id="aiorocket2.models.Cheque.ref_reward_per_user"></a>

#### ref\_reward\_per\_user

amount of referral user reward

<a id="aiorocket2.models.Cheque.captcha_enabled"></a>

#### captcha\_enabled

enable / disable cheque captcha

<a id="aiorocket2.models.Cheque.disabled_languages"></a>

#### disabled\_languages

Disable languages

<a id="aiorocket2.models.Cheque.enabled_countries"></a>

#### enabled\_countries

Enabled countries

<a id="aiorocket2.models.Cheque.for_premium"></a>

#### for\_premium

Only users with Telegram Premium can activate this cheque

<a id="aiorocket2.models.Cheque.for_new_users_only"></a>

#### for\_new\_users\_only

Only new users can activate this cheque

<a id="aiorocket2.models.Cheque.linked_wallet"></a>

#### linked\_wallet

Only users with connected wallets can activate this cheque

<a id="aiorocket2.models.Cheque.activations"></a>

#### activations

How many times cheque is activate

<a id="aiorocket2.models.Cheque.ref_rewards"></a>

#### ref\_rewards

How many times referral reward is payed

<a id="aiorocket2.models.Cheque.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "Cheque"
```

Build Cheque from API JSON object.

<a id="aiorocket2.models.TgResource"></a>

## TgResource Objects

```python
@dataclass
class TgResource(Base)
```

Represents a TgResourse entity returned by the xRocket Pay API.

<a id="aiorocket2.models.TgResource.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "TgResource"
```

Build Cheque from API JSON object.

<a id="aiorocket2.models.PaginatedCheque"></a>

## PaginatedCheque Objects

```python
@dataclass
class PaginatedCheque(Base)
```

Represents a PaginatedCheque entity returned by the xRocket Pay API.

<a id="aiorocket2.models.PaginatedCheque.total"></a>

#### total

Total times

<a id="aiorocket2.models.PaginatedCheque.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "PaginatedCheque"
```

Build PaginatedCheque from API JSON object.

<a id="aiorocket2.models.DateTimeStr"></a>

## DateTimeStr Objects

```python
@dataclass
class DateTimeStr(str, Base)
```

Time object, to comfortable get time from the api

<a id="aiorocket2.models.Invoice"></a>

## Invoice Objects

```python
@dataclass
class Invoice(Base)
```

Represents a Invoice entity returned by the xRocket Pay API.

<a id="aiorocket2.models.Invoice.id"></a>

#### id

Invoice ID

<a id="aiorocket2.models.Invoice.amount"></a>

#### amount

Amount of invoice

<a id="aiorocket2.models.Invoice.min_payment"></a>

#### min\_payment

Min payment of invoice

<a id="aiorocket2.models.Invoice.total_activations"></a>

#### total\_activations

Total activations of invoice

<a id="aiorocket2.models.Invoice.activations_left"></a>

#### activations\_left

Activations left of invoice

<a id="aiorocket2.models.Invoice.description"></a>

#### description

Invoice description

<a id="aiorocket2.models.Invoice.hidden_message"></a>

#### hidden\_message

Message that will be displayed after invoice payment

<a id="aiorocket2.models.Invoice.payload"></a>

#### payload

Any data that is attached to invoice

<a id="aiorocket2.models.Invoice.callback_url"></a>

#### callback\_url

url that will be set for Return button after invoice is paid

<a id="aiorocket2.models.Invoice.comments_enabled"></a>

#### comments\_enabled

Allow comments for invoice

<a id="aiorocket2.models.Invoice.created"></a>

#### created

(date-time) When invoice was created

<a id="aiorocket2.models.Invoice.paid"></a>

#### paid

(date-time) When invoice was paid

<a id="aiorocket2.models.Invoice.expired_in"></a>

#### expired\_in

Invoice expire time in seconds, max 1 day, 0 - none expired

<a id="aiorocket2.models.Invoice.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "Invoice"
```

Build Invoice from API JSON object.

<a id="aiorocket2.models.PaginatedInvoice"></a>

## PaginatedInvoice Objects

```python
@dataclass
class PaginatedInvoice(Base)
```

Represents a PaginatedInvoice entity returned by the xRocket Pay API.

<a id="aiorocket2.models.PaginatedInvoice.total"></a>

#### total

Total times

<a id="aiorocket2.models.PaginatedInvoice.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "PaginatedInvoice"
```

Build PaginatedInvoice from API JSON object.

<a id="aiorocket2.models.WithdrawalFee"></a>

## WithdrawalFee Objects

```python
@dataclass
class WithdrawalFee(Base)
```

Represents a WithdrawalFee entity returned by the xRocket Pay API.

<a id="aiorocket2.models.WithdrawalFee.currency"></a>

#### currency

ID of main currency for token

<a id="aiorocket2.models.WithdrawalFee.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "WithdrawalFee"
```

Build WithdrawalFee from API JSON object.

<a id="aiorocket2.models.Currency"></a>

## Currency Objects

```python
@dataclass
class Currency(Base)
```

Represents a Currency entity returned by the xRocket Pay API.

<a id="aiorocket2.models.Currency.currency"></a>

#### currency

ID of currency, use in Rocket Pay Api

<a id="aiorocket2.models.Currency.name"></a>

#### name

Name of currency

<a id="aiorocket2.models.Currency.min_transfer"></a>

#### min\_transfer

Minimal amount for transfer

<a id="aiorocket2.models.Currency.min_cheque"></a>

#### min\_cheque

Minimal amount for cheque

<a id="aiorocket2.models.Currency.min_invoice"></a>

#### min\_invoice

Minimal amount for invoice

<a id="aiorocket2.models.Currency.min_withdraw"></a>

#### min\_withdraw

Minimal amount for withdrawals

<a id="aiorocket2.models.Currency.from_api"></a>

#### from\_api

```python
@classmethod
def from_api(cls, j: Mapping[str, Any]) -> "Currency"
```

Build Currency from API JSON object.

<a id="aiorocket2.tags.app"></a>

# aiorocket2.tags.app

Tag App from the API

<a id="aiorocket2.tags.app.App"></a>

## App Objects

```python
class App()
```

Tag App from the API

<a id="aiorocket2.tags.app.App.get_info"></a>

#### get\_info

```python
async def get_info() -> Info
```

Returns information about your application

**Returns**:

- `Info` - information about your application

<a id="aiorocket2.tags.app.App.send_transfer"></a>

#### send\_transfer

```python
async def send_transfer(tg_user_id: int,
                        currency: str,
                        amount: float,
                        transfer_id: str,
                        description: Optional[str] = None) -> Transfer
```

Make transfer of funds to another user

**Arguments**:

- `tg_user_id` _int_ - Telegram user ID. If we dont have this user in DB, we will fail transaction with error: 400 - User not found
- `currency` _str_ - Currency of transfer, info `xRocketClient.get_available_currencies()`
- `amount` _float_ - Transfer amount. 9 decimal places, others cut off
- `transfer_id` _str_ - Unique transfer ID in your system to prevent double spends
- `description` _str_ - Transfer description
  

**Returns**:

  Transfer:

<a id="aiorocket2.tags.app.App.create_withdrawal"></a>

#### create\_withdrawal

```python
async def create_withdrawal(network: Network, address: str, currency: str,
                            amount: float, withdrawal_id: str,
                            comment: str) -> Withdrawal
```

Make withdrawal of funds to external wallet

**Arguments**:

- `network` _Network_ - Network code.
- `address` _str_ - Withdrawal address. E.g. `EQB1cmpxb3R-YLA3HLDV01Rx6OHpMQA_7MOglhqL2CwJx_dz`
- `currency` _str_ - Currency code
- `amount` _float_ - Withdrawal amount. 9 decimal places, others cut off
- `withdrawal_id` _str_ - Unique withdrawal ID in your system to prevent double spends. Must not be longer than 50
- `comment` _str_ - Withdrawal comment. Must not be longer than 50
  

**Returns**:

  Withdrawal:

<a id="aiorocket2.tags.app.App.get_withdrawal"></a>

#### get\_withdrawal

```python
async def get_withdrawal(withdrawal_id: str) -> Withdrawal
```

Returns withdrawal info

**Arguments**:

- `withdrawal_id` _str_ - Unique withdrawal ID in your system.
  

**Returns**:

  Withdrawal:

<a id="aiorocket2.tags.app.App.get_withdrawal_status"></a>

#### get\_withdrawal\_status

```python
async def get_withdrawal_status(withdrawal_id: str) -> WithdrawalStatus
```

Returns withdrawal status

**Arguments**:

- `withdrawal_id` _str_ - Unique withdrawal ID in your system.
  

**Returns**:

  WithdrawalStatus:

<a id="aiorocket2.tags.app.App.get_withdrawal_fees"></a>

#### get\_withdrawal\_fees

```python
async def get_withdrawal_fees(
        currency: Optional[str] = None) -> List[WithdrawalCoin]
```

Returns withdrawal fees

**Arguments**:

- `currency` _str_ - Coin for get fees, optional
  

**Returns**:

  List[WithdrawalCoin]:

<a id="aiorocket2.tags.currencies"></a>

# aiorocket2.tags.currencies

Tag currencies from the API

<a id="aiorocket2.tags.currencies.Currencies"></a>

## Currencies Objects

```python
class Currencies()
```

Tag currencies from the API

<a id="aiorocket2.tags.currencies.Currencies.get_available_currencies"></a>

#### get\_available\_currencies

```python
async def get_available_currencies() -> List[Currency]
```

Returns available currencies

**Returns**:

- `List[Currency]` - List of available currencies

<a id="aiorocket2.tags.health"></a>

# aiorocket2.tags.health

Tag health from the API

<a id="aiorocket2.tags.health.Health"></a>

## Health Objects

```python
class Health()
```

Tag health from the API

<a id="aiorocket2.tags.health.Health.check_health"></a>

#### check\_health

```python
async def check_health() -> Status
```

Return API Status

**Returns**:

  Status:

<a id="aiorocket2.tags.multi_cheque"></a>

# aiorocket2.tags.multi\_cheque

<a id="aiorocket2.tags.multi_cheque.MultiCheque"></a>

## MultiCheque Objects

```python
class MultiCheque()
```

<a id="aiorocket2.tags.multi_cheque.MultiCheque.create_multi_cheque"></a>

#### create\_multi\_cheque

```python
async def create_multi_cheque(
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
        enabled_countries: List["Country"] = None) -> Cheque
```

Create multi-cheque

**Arguments**:

- `currency` _str_ - Currency of transfer, info `xRocketClient.get_available_currencies()`
- `cheque_per_user` _float_ - Cheque amount for one user. 9 decimal places, others cut off
- `users_number` _int_ - Number of users to save multicheque. 0 decimal places. Minimum 1
- `ref_program` _int_ - Referral program percentage (%). 0 decimal places. Minimum 0. Maximum 100
- `password` _str_ - Optional. Password for cheque. Max length 100
- `description` _str_ - Optional. Description for cheque. Max length 1000
- `send_notifications` _bool_ - Optional. Send notifications about activations. Default True
- `enable_captcha` _bool_ - Optional. Enable captcha. Default True
- `telegram_resources_ids` _List of int or str_ - IDs of telegram resources (groups, channels, private groups)
- `for_premium` _bool_ - Optional. Only users with Telegram Premium can activate this cheque. Default False
- `linked_wallet` _bool_ - Optional. Only users with linked wallet can activate this cheque. Default False
- `disabled_languages` _List of str_ - Optional. Disable languages
- `enabled_countries` _List of Country_ - Optional. Enabled countries
  

**Returns**:

  Cheque:

<a id="aiorocket2.tags.multi_cheque.MultiCheque.get_multi_cheques"></a>

#### get\_multi\_cheques

```python
async def get_multi_cheques(limit: int = 100,
                            offset: int = 0) -> PaginatedCheque
```

Get list of multi-cheques

**Arguments**:

- `limit` _int_ - Minimum 1. Maximum 1000. Default 100
- `offset` _int_ - Minimum 0. Default 0
  

**Returns**:

  PaginatedCheque:

<a id="aiorocket2.tags.multi_cheque.MultiCheque.get_multi_cheque"></a>

#### get\_multi\_cheque

```python
async def get_multi_cheque(cheque_id: int) -> Cheque
```

Get multi-cheque info

**Arguments**:

- `cheque_id` _str_ - Cheque ID
  

**Returns**:

  Cheque:

<a id="aiorocket2.tags.multi_cheque.MultiCheque.edit_multi_cheque"></a>

#### edit\_multi\_cheque

```python
async def edit_multi_cheque(
        cheque_id: int,
        password: str = None,
        description: str = None,
        send_notifications: bool = None,
        enable_captcha: bool = None,
        telegram_resources_ids: List[Union[int, str]] = None,
        for_premium: bool = None,
        linked_wallet: bool = None,
        disabled_languages: List[str] = None,
        enabled_countries: List["Country"] = None) -> Cheque
```

Edit multi-cheque

**Arguments**:

  cheque_id (int):
- `password` - (str): Optional. Password for cheque. Max lenght 100
- `description` _str_ - Optional. Description for cheque. Max lenght 1000
- `send_notifications` _bool_ - Optional. Send notifications about activations. Default True
- `enable_captcha` _bool_ - Optional. Enable captcha. Default True
- `telegram_resources_ids` _List of int or str_ - IDs of telegram resources (groups, channels, private groups)
- `for_premium` _bool_ - Optional. Only users with Telegram Premium can activate this cheque. Default False
- `linked_wallet` _bool_ - Optional. Only users with linked wallet can activate this cheque. Default False
- `disabled_languages` _List of str_ - Optional. Disable languages
- `enabled_countries` _List of Country_ - Optional. Enabled countries
  

**Returns**:

  Cheque:

<a id="aiorocket2.tags.multi_cheque.MultiCheque.delete_multi_cheque"></a>

#### delete\_multi\_cheque

```python
async def delete_multi_cheque(cheque_id: str) -> True
```

Delete multi-cheque

**Arguments**:

- `cheque_id` _str_ - Cheque ID
  

**Returns**:

- `True` - on success, otherwise raises xRocketAPIError

<a id="aiorocket2.tags.tg_invoices"></a>

# aiorocket2.tags.tg\_invoices

Tag tg-invoices from the API

<a id="aiorocket2.tags.tg_invoices.TgInvoices"></a>

## TgInvoices Objects

```python
class TgInvoices()
```

Tag tg-invoices from the API

<a id="aiorocket2.tags.tg_invoices.TgInvoices.create_invoice"></a>

#### create\_invoice

```python
async def create_invoice(amount: float,
                         min_payment: float,
                         num_payments: int,
                         currency: str,
                         description: str = None,
                         hidden_message: str = None,
                         comments_enabled: bool = False,
                         callback_url: str = None,
                         payload: str = None,
                         expired_in: int = 0,
                         platform_id: str = None) -> Invoice
```

Create invoice

**Arguments**:

- `amount` _float_ - Invoice amount. 9 decimal places, others cut off. Minimum 0. Maximum 1_000_000
- `min_payment` _float_ - Min payment only for multi invoice if invoice amount is None. Minimum 0. Maximum 1_000_000
- `num_payments` _int_ - Num payments for invoice. Minimum 0. Maximum 1_000_000
- `currency` _str_ - Currency of transfer, info `xRocketClient.get_available_currencies()`
- `description` _str_ - Optional. Description for invoice. Maximum 1000
- `hidden_message` _str_ - Optional. Hidden message after invoice is paid. Maximum 2000
- `comments_enabled` _bool_ - Optional. Allow comments. Default False
- `callback_url` _str_ - Optional. Url for Return button after invoice is paid. Maximum 500
- `payload` _str_ - Optional. Any data. Invisible to user, will be returned in callback. Maximum 4000
- `expired_in` _int_ - Optional. Invoice expire time in seconds, max 1 day, 0 - none expired. Minimum 0. Maximum 86400. Default 0
- `platform_id` _str_ - Optional. Platform identifier
  

**Returns**:

  Invoice:

<a id="aiorocket2.tags.tg_invoices.TgInvoices.get_invoices"></a>

#### get\_invoices

```python
async def get_invoices(limit: int = 100, offset: int = 0) -> PaginatedInvoice
```

Get list of invoices

**Arguments**:

- `limit` _int_ - Minimum 1. Maximum 1000. Default 100
- `offset` _int_ - Minimum 0. Default 0
  

**Returns**:

  PaginatedInvoice:

<a id="aiorocket2.tags.tg_invoices.TgInvoices.get_invoice"></a>

#### get\_invoice

```python
async def get_invoice(invoice_id: int) -> Invoice
```

Get invoice

**Arguments**:

- `invoice_id` _str_ - Invoice ID
  

**Returns**:

  Invoice:

<a id="aiorocket2.tags.tg_invoices.TgInvoices.delete_invoice"></a>

#### delete\_invoice

```python
async def delete_invoice(invoice_id: int) -> True
```

Delete invoice

**Arguments**:

- `invoice_id` _int_ - Invoice ID
  

**Returns**:

- `True` - on success otherwise raises xRocketAPIError

<a id="aiorocket2.tags.version"></a>

# aiorocket2.tags.version

Tag Version from the API

<a id="aiorocket2.tags.version.Version"></a>

## Version Objects

```python
class Version()
```

Tag version from the API

<a id="aiorocket2.tags.version.Version.get_version"></a>

#### get\_version

```python
async def get_version() -> str
```

Returns current version of API. You may use it as healthcheck

**Returns**:

- `str` - Version string, e.g., "1.3.1".

<a id="aiorocket2.tags.withdrawal_link"></a>

# aiorocket2.tags.withdrawal\_link

Tag withdrawal-link from the API

<a id="aiorocket2.tags.withdrawal_link.WithdrawalLink"></a>

## WithdrawalLink Objects

```python
class WithdrawalLink()
```

Tag Withdrawal-link from the API

<a id="aiorocket2.tags.withdrawal_link.WithdrawalLink.get_withdrawal_link"></a>

#### get\_withdrawal\_link

```python
async def get_withdrawal_link(currency: str,
                              network: Network,
                              address: str,
                              amount: float = 0,
                              comment: str = None,
                              platform: str = None) -> Optional[str]
```

Get withdrawal link

**Arguments**:

- `currency` _str_ - Currency code (`xRocketClient.get_available_currencies()`)
- `network` _Network_ - Network code
- `address` _str_ - Target withdrawal address
- `amount` _float_ - Optional. Withdrawal amount. Default 0
- `comment` _str_ - Optional. Withdrawal comment
- `platform` _str_ - Optional. Platform identifier (optional, use only if provided by xRocket)
  

**Returns**:

- `str` - Telegram app link

<a id="aiorocket2.tags"></a>

# aiorocket2.tags

The API is splitted by tags. Here is the same splitting

<a id="aiorocket2.tags.Tags"></a>

## Tags Objects

```python
class Tags(Version, App, MultiCheque, TgInvoices, WithdrawalLink, Currencies,
           Health)
```

General class to join all tags together

<a id="aiorocket2.utils"></a>

# aiorocket2.utils

additional functions used by aiorocket2

<a id="aiorocket2.utils.generate_idempotency_id"></a>

#### generate\_idempotency\_id

```python
def generate_idempotency_id() -> str
```

Generate a simple idempotency identifier based on the current timestamp.

The xRocket Pay API accepts `transferId` / `withdrawalId` for idempotency.

<a id="aiorocket2.utils.backoff_sleep"></a>

#### backoff\_sleep

```python
async def backoff_sleep(attempt: int, base: float) -> None
```

Sleep using exponential backoff for the given attempt number (0-based).

<a id="aiorocket2.version"></a>

# aiorocket2.version

version of aiorocket2

