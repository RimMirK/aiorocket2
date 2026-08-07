# Quickstart

Install with pip:

```bash
pip install aiorocket2
```

Minimal working example (create an invoice):

```python
import asyncio
from aiorocket2 import xRocketClient

async def main():
    client = xRocketClient(api_key="YOUR_API_KEY", testnet=True)
    invoice = await client.create_invoice(currency="TON", amount=0.01, description="Test payment")
    print("Invoice id:", invoice.id)

asyncio.run(main())
```

Notes:

- Use `testnet=True` during development to avoid real transfers.
- This package is async-first — use `asyncio.run(...)` in simple scripts or integrate with your bot's event loop.
- If a function expects an enum (see `aiorocket2.enums`) prefer passing enum members (for example `Network.TON`).

Common short flows

- Create a multi-cheque (many users share a single cheque):

```python
async with xRocketClient(api_key="KEY") as client:
    cheque = await client.create_multi_cheque(currency="TON", cheque_per_user=0.001, users_number=10, ref_program=5)
    print(cheque.id, cheque.url)
```

- Create a withdrawal link (on-chain withdrawal via a link):

```python
from aiorocket2.enums import Network

async with xRocketClient(api_key="KEY") as client:
    link = await client.get_withdrawal_link(currency="TON", network=Network.TON, address="EQ...", amount=0.1)
    print(link)
```

Where to go next

- Read the [Methods guide](guides/methods.md) for practical parameter details and common mistakes.
- Browse the [auto-generated API reference](api/index.md) for full signatures and models.
