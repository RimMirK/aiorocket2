# aiorocket

[Documentation](https://aiorocket.rimmirk.pp.ua) | [Issues](https://github.com/RimMirK/aiorocket/issues) | [Dev Branch](https://github.com/RimMirK/aiorocket/tree/dev)

Asynchronous Python client for **xRocket API**. Provides full access to the API, passing all parameters directly.

## DEV installation

```bash
pip install git+https://github.com/<your-username>/aiorocket.git@dev
````

> Requires Python 3.11 or higher.

## Quick Start

```python
import asyncio
from aiorocket import xRocketClient

async def main():
    xrocket = xRocketClient(api_key="YOUR_API_KEY")
    
    # Example: get balance
    balance = await xrocket.get_balance()
    print(balance)

asyncio.run(main())
```

## Features

* Asynchronous API access with `asyncio`
* Direct parameter mapping from xRocket API
* Easy installation via pip from `dev` branch
* Full API coverage

## Authors

* aiorocket 2.x: [RimMirK](https://github.com/RimMirK)
* Original author (aiorocket 1.x): [Sovenok-Hacker](https://github.com/Sovenok-Hacker)

## License

This project is licensed under the **GNU GPLv3** License.
See the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) for details.


