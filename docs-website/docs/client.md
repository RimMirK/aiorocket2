---
sidebar_position: 2
title: Methods
---

---

### `__init__`

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

---

### `get_info`

```python
async def get_info() -> Info
```

Returns information about your application

**Returns**:

- `Info` - information about your application


---

### `send_transfer`

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
- `currency` _str_ - Currency of transfer, info [`xRocketClient.get_available_currencies()`](client#get_available_currencies)
- `amount` _float_ - Transfer amount. 9 decimal places, others cut off
- `transfer_id` _str_ - Unique transfer ID in your system to prevent double spends
- `description` _str_ - Transfer description
  

**Returns**:
    `Transfer`


---

### `create_withdrawal`

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
    `Withdrawal`


---

### `get_withdrawal`

```python
async def get_withdrawal(withdrawal_id: str) -> Withdrawal
```

Returns withdrawal info

**Arguments**:

- `withdrawal_id` _str_ - Unique withdrawal ID in your system.
  

**Returns**:
    `Withdrawal`


---

### `get_withdrawal_status`

```python
async def get_withdrawal_status(withdrawal_id: str) -> WithdrawalStatus
```

Returns withdrawal status

**Arguments**:

- `withdrawal_id` _str_ - Unique withdrawal ID in your system.
  

**Returns**:
    `WithdrawalStatus`


---

### `get_withdrawal_fees`

```python
async def get_withdrawal_fees(
        currency: Optional[str] = None) -> List[WithdrawalCoin]
```

Returns withdrawal fees

**Arguments**:

- `currency` _str_ - Coin for get fees, optional
  

**Returns**:
    `List[WithdrawalCoin]`



---

### `get_available_currencies`

```python
async def get_available_currencies() -> List[Currency]
```

Returns available currencies

**Returns**:

- `List[Currency]` - List of available currencies


---

### `check_health`

```python
async def check_health() -> Status
```

Return API Status

**Returns**:
    `Status`









```python
class MultiCheque()
```


---

### `create_multi_cheque`

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

- `currency` _str_ - Currency of transfer, info [`xRocketClient.get_available_currencies()`](client#get_available_currencies)
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
    `Cheque`


---

### `get_multi_cheques`

```python
async def get_multi_cheques(limit: int = 100,
                            offset: int = 0) -> PaginatedCheque
```

Get list of multi-cheques

**Arguments**:

- `limit` _int_ - Minimum 1. Maximum 1000. Default 100
- `offset` _int_ - Minimum 0. Default 0
  

**Returns**:
    `PaginatedCheque`


---

### `get_multi_cheque`

```python
async def get_multi_cheque(cheque_id: int) -> Cheque
```

Get multi-cheque info

**Arguments**:

- `cheque_id` _str_ - Cheque ID
  

**Returns**:
    `Cheque`


---

### `edit_multi_cheque`

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

- `cheque_id` (int):
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
    `Cheque`


---

### `delete_multi_cheque`

```python
async def delete_multi_cheque(cheque_id: str) -> True
```

Delete multi-cheque

**Arguments**:

- `cheque_id` _str_ - Cheque ID
  

**Returns**:

- `True` - on success, otherwise raises xRocketAPIError



---

### `create_invoice`

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
- `currency` _str_ - Currency of transfer, info [`xRocketClient.get_available_currencies()`](client#get_available_currencies)
- `description` _str_ - Optional. Description for invoice. Maximum 1000
- `hidden_message` _str_ - Optional. Hidden message after invoice is paid. Maximum 2000
- `comments_enabled` _bool_ - Optional. Allow comments. Default False
- `callback_url` _str_ - Optional. Url for Return button after invoice is paid. Maximum 500
- `payload` _str_ - Optional. Any data. Invisible to user, will be returned in callback. Maximum 4000
- `expired_in` _int_ - Optional. Invoice expire time in seconds, max 1 day, 0 - none expired. Minimum 0. Maximum 86400. Default 0
- `platform_id` _str_ - Optional. Platform identifier
  

**Returns**:
    `Invoice`


---

### `get_invoices`

```python
async def get_invoices(limit: int = 100, offset: int = 0) -> PaginatedInvoice
```

Get list of invoices

**Arguments**:

- `limit` _int_ - Minimum 1. Maximum 1000. Default 100
- `offset` _int_ - Minimum 0. Default 0
  

**Returns**:
    `PaginatedInvoice`


---

### `get_invoice`

```python
async def get_invoice(invoice_id: int) -> Invoice
```

Get invoice

**Arguments**:

- `invoice_id` _str_ - Invoice ID
  

**Returns**:
    `Invoice`


---

### `delete_invoice`

```python
async def delete_invoice(invoice_id: int) -> True
```

Delete invoice

**Arguments**:

- `invoice_id` _int_ - Invoice ID
  

**Returns**:

- `True` - on success otherwise raises xRocketAPIError



---

### `get_version`

```python
async def get_version() -> str
```

Returns current version of API. You may use it as healthcheck

**Returns**:

- `str` - Version string, e.g., "1.3.1".



---

### `get_withdrawal_link`

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

- `currency` _str_ - Currency code ([`xRocketClient.get_available_currencies()`](client#get_available_currencies))
- `network` _Network_ - Network code
- `address` _str_ - Target withdrawal address
- `amount` _float_ - Optional. Withdrawal amount. Default 0
- `comment` _str_ - Optional. Withdrawal comment
- `platform` _str_ - Optional. Platform identifier (optional, use only if provided by xRocket)
  

**Returns**:

- `str` - Telegram app link



# aiorocket2.tags

The API is splitted by tags. Here is the same splitting
