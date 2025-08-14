# aiorocket

[Documentation](https://aiorocket.rimmirk.pp.ua) | [Issues](https://github.com/RimMirK/aiorocket/issues) | [Dev Branch](https://github.com/RimMirK/aiorocket/tree/dev)

Asynchronous Python client for **xRocket API**. Provides full access to the API, passing all parameters directly.

## Installation

```bash
# IDK How to download this shit, sorry
```

> Requires Python 3.11 or higher.

## Getting API Key

You need an API key from the xRocket Payment System ([@xRocket](https://t.me/xRocket), [@xrocket_testnet_bot](https://t.me/xrocket_testnet_bot) for testnet). Open the bot and go to: **Rocket Pay** > **Create App** > **API token**.

## Quick Start

```python
import asyncio
from aiorocket import xRocketClient

async def main():
    xrocket = xRocketClient(api_key="YOUR_API_KEY")
    
    # Example: get app info
    info = await xrocket.get_info()
    print(info)

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


