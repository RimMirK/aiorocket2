# Methods guide — practical usage

This page focuses on the most common methods for Telegram payment integrations.

Overview
--------

- `create_invoice(...)` — create a single invoice (payable by a user).
- `create_multi_cheque(...)` — create a multi-cheque for many users.
- `get_withdrawal_link(...)` — generate a withdrawal link for on-chain withdraws.

General rules
-------------

- Where a parameter expects an `Enum` (see `aiorocket2.enums`), pass the enum member (example: `Network.TON`). Methods often use `.value` internally, but passing enum improves clarity and avoids mistakes.
- Numeric amounts: the API uses high precision (up to 9 decimals). Use Python `float` for small scripts; consider `decimal.Decimal` for strict precision.
- Strings such as `currency` usually expect currency code (e.g. `"TON"`). Prefer using the library helpers like `client.get_available_currencies()`.

create_invoice
--------------

Signature example (auto-generated):

```py
async def create_invoice(self, currency: str, amount: float = None, min_payment: float = None, ... ) -> Invoice
```

What you need to know:

- `currency` (str): Currency code. Use `client.get_available_currencies()` to list valid currencies.
- `amount` (float): Optional. If provided the invoice has fixed amount.
- `expired_in` (int): Expiry in seconds, `0` — never expire.
- `payload` (str): Arbitrary opaque value returned in callbacks — useful to store your internal identifiers.

Example:

```python
async with xRocketClient(api_key="KEY") as client:
    inv = await client.create_invoice(currency="TON", amount=0.01, description="Donation")
    print(inv.id, inv.url)
```

Common mistakes / troubleshooting:

- Passing wrong currency code — use `get_available_currencies()` or check the `enums`.
- Passing enums as plain strings in some multi-field params — prefer enum members.

create_multi_cheque
-------------------

Signature example:

```py
async def create_multi_cheque(self, currency: str, cheque_per_user: float, users_number: int, ref_program: int, ... ) -> Cheque
```

Key parameters:

- `cheque_per_user` (float): Amount per user, up to 9 decimal places.
- `users_number` (int): Number of activations users can take.
- `enabled_countries` (List[Country]): Prefer passing `Country` enum members (e.g., `[Country.RU, Country.US]`).

Example:

```python
from aiorocket2 import xRocketClient
from aiorocket2.enums import Country

async with xRocketClient(api_key="KEY") as client:
    chk = await client.create_multi_cheque(currency="TON", cheque_per_user=0.001, users_number=50, ref_program=0, enabled_countries=[Country.US, Country.GB])
    print(chk.id, chk.inviteUrl)
```

Common mistakes:

- Passing raw country codes as strings instead of `Country` enum members — the library will transform enums to their `.value`, but using the enums in code prevents typos.

get_withdrawal_link
-------------------

Signature example:

```py
async def get_withdrawal_link(self, currency: str, network: Network, address: str, amount: float = 0, ...) -> Optional[str]
```

Notes:

- `network` should be a `Network` enum member (e.g., `Network.TON`).
- The method returns a Telegram app link (string) or raises `xRocketAPIError` on failure.

Example:

```python
from aiorocket2.enums import Network

async with xRocketClient(api_key="KEY") as client:
    link = await client.get_withdrawal_link(currency="TON", network=Network.TON, address="EQ...", amount=0.05)
    print(link)
```

Common mistakes:

- Passing network as string — use `Network.TON` to avoid typos.
- Passing an invalid address — the API may return an error which becomes an `xRocketAPIError` in the client.

Next steps
----------

- Browse the auto-generated [API reference](../api/index.md) for full signatures and model descriptions. I will update docstrings where needed so those pages include more examples and parameter notes.
- If you want, I can add small runnable example scripts under `docs/examples/` for copy-paste use in your bots.
