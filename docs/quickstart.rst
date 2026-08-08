Quickstart
==========

Install with pip::

   pip install aiorocket2

Minimal working example (create an invoice)::

   import asyncio
   from aiorocket2 import xRocketClient

   async def main():
       client = xRocketClient(api_key="YOUR_API_KEY", testnet=True)
       invoice = await client.create_invoice(currency="TON", amount=0.01, description="Test payment")
       print("Invoice id:", invoice.id)

   asyncio.run(main())

Notes
-----

- Use ``testnet=True`` during development to avoid real transfers.
- The package is async-first — integrate with your bot event loop or use ``asyncio.run(...)`` in scripts.
- When a parameter expects an enum (see ``aiorocket2.enums``) prefer passing enum members (``Network.TON``).

See also: :doc:`/guides/methods` and the :doc:`/api/index`.
