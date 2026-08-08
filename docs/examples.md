# Examples

## Basic usage

```python
import asyncio
from aiorocket2 import xRocketClient

async def main():
    async with xRocketClient(api_key="YOUR_API_KEY") as client:
        info = await client.get_info()
        print(info.name)
        print(info.balances)

asyncio.run(main())
```

## List available currencies

```python
import asyncio
from aiorocket2 import xRocketClient

async def main():
    async with xRocketClient(api_key="YOUR_API_KEY", testnet=True) as client:
        currencies = await client.get_available_currencies()
        for currency in currencies:
            print(currency.currency, currency.min_transfer)

asyncio.run(main())
```

## Create an invoice

```python
import asyncio
from aiorocket2 import xRocketClient

async def main():
    async with xRocketClient(api_key="YOUR_API_KEY") as client:
        invoice = await client.create_invoice(
            currency="TON",
            amount=0.01,
            description="Demo invoice",
            payload="order-1234",
            expired_in=3600,
        )
        print("Invoice URL:", invoice.link)
        print("Invoice ID:", invoice.id)

asyncio.run(main())
```

## Create a multi-cheque

```python
import asyncio
from aiorocket2 import xRocketClient
from aiorocket2.enums import Country

async def main():
    async with xRocketClient(api_key="YOUR_API_KEY") as client:
        cheque = await client.create_multi_cheque(
            currency="TON",
            cheque_per_user=0.001,
            users_number=50,
            ref_program=0,
            description="Event reward",
            enabled_countries=[Country.US, Country.GB],
        )
        print("Cheque link:", cheque.link)
        print("Max activations:", cheque.users)

asyncio.run(main())
```

## Get withdrawal link

```python
import asyncio
from aiorocket2 import xRocketClient
from aiorocket2.enums import Network

async def main():
    async with xRocketClient(api_key="YOUR_API_KEY") as client:
        link = await client.get_withdrawal_link(
            currency="TON",
            network=Network.TON,
            address="EQ...",
            amount=0.05,
            comment="Payout for user",
        )
        print("Withdrawal link:", link)

asyncio.run(main())
```

## Health check

```python
import asyncio
from aiorocket2 import xRocketClient

async def main():
    async with xRocketClient(api_key="YOUR_API_KEY") as client:
        status = await client.check_health()
        print("API status:", status)

asyncio.run(main())
```
