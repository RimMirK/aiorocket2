# aiorocket

[Documentation](https://github.com/<your-username>/aiorocket/wiki) | [Issues](https://github.com/<your-username>/aiorocket/issues) | [Dev Branch](https://github.com/<your-username>/aiorocket/tree/dev)

Asynchronous Python client for **xRocket API**. Provides full access to the API, passing all parameters directly.

## Installation

```bash
pip install git+https://github.com/<your-username>/aiorocket.git@dev
````

> Requires Python 3.11 or higher.

## Quick Start

```python
import asyncio
from aiorocket import Client

async def main():
    client = Client(api_key="YOUR_API_KEY")
    
    # Example: get balance
    balance = await client.get_balance()
    print(balance)

asyncio.run(main())
```

## Features

* Asynchronous API access with `asyncio`
* Direct parameter mapping from xRocket API
* Easy installation via pip from `dev` branch
* Full API coverage

## Authors

* Original author: [OriginalDev](https://github.com/originaldev)
* Current development and rewrite: [YourUsername](https://github.com/<your-username>)

## License

This project is licensed under the **GNU GPLv3** License.
See the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) for details.


