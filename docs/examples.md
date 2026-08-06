# Examples

## Basic usage

```python
import asyncio
from aiorocket2 import xRocketClient

async def main():
    client = xRocketClient(api_key="YOUR_API_KEY")
    info = await client.get_info()
    print(info)

asyncio.run(main())
```

## Create an invoice

```python
import asyncio
from aiorocket2 import xRocketClient

async def main():
    client = xRocketClient(api_key="YOUR_API_KEY")
    invoice = await client.create_invoice(
        amount=10,
        min_payment=0,
        num_payments=1,
        currency="USDT",
        description="Demo invoice",
    )
    print(invoice.link)

asyncio.run(main())
```
