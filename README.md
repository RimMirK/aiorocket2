# ![aiorocket2 🚀](.github/logo+name.png)

[![PyPI](https://img.shields.io/pypi/v/aiorocket2?color=blue&logo=python&style=flat-square)](https://pypi.org/project/aiorocket2/)
[![Python Version](https://img.shields.io/pypi/pyversions/aiorocket2?style=flat-square)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPLv3-blue?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0.en.html)
[![Documentation](https://img.shields.io/badge/docs-online-brightgreen?style=flat-square)](https://aiorocket2.rimmirk.pp.ua)
[![Issues](https://img.shields.io/github/issues/RimMirK/aiorocket2?style=flat-square)](https://github.com/RimMirK/aiorocket2/issues)

**aiorocket2** is an asynchronous Python client for the **xRocket Pay API**, providing full access to all methods and parameters of the payment system.  
All types, enums, and data structures are mirrored as closely as possible to the original API.

---

## 🚀 Features

- Complete wrapper for all xRocket API methods  
- Asynchronous access via `asyncio`  
- Full typing support and enums  
- Direct parameter mapping from API  
- Production-ready and test-friendly  

---

## 📦 Installation

```bash
pip install aiorocket2
```

> Requires Python 3.7+

---

## 🔑 Getting an API Key

1. Open the bot [@xRocket](https://t.me/xRocket) or [@xrocket\_testnet\_bot](https://t.me/xrocket_testnet_bot) for the testnet
2. Go to: **xRocket API -> xRocket Pay → Create App → API token**
3. Copy the token and use it in your code

---

## ⚡ Quick Start

```python
import asyncio
from aiorocket2 import xRocketClient

async def main():
    client = xRocketClient(api_key="YOUR_API_KEY")
    
    # Get application info
    info = await client.get_info()
    print(info)
    
    # Example: create a invoice
    invoice = await client.create_invoice(
        amount=10, # 10 USDT to pay
        min_payment=0, # For single payment pass 0
        num_payments=1, # For single payment pass 1
        currency="USDT",
        description="Buy some products",
        hidden_message="Thanks for payment!", # this will appear to the payer after payment
        comments_enabled=True
    )
    print(invoice.link)

asyncio.run(main())
```

> All library methods mirror the xRocket API exactly, including types, required and optional parameters.

---

## 📚 Documentation

Full documentation is available online: [aiorocket2 Docs](https://aiorocket2.rimmirk.pp.ua)
Includes:

* Description of all API methods
* Usage examples
* List of all enums and data structures

---

## 👨‍💻 Authors

* [RimMirK](https://github.com/RimMirK)

---

## 📝 License

This project is licensed under **GNU GPLv3**.
[Full license text](https://www.gnu.org/licenses/gpl-3.0.en.html)
