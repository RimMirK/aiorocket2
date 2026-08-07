get_withdrawal_link — detailed
==============================

Signature
---------

.. code-block:: python

   async def get_withdrawal_link(self, currency: str, network: Network, address: str, amount: float = 0, comment: str = None, platform: str = None) -> Optional[str]

Key notes
---------

- ``network`` must be a ``Network`` enum member (e.g., ``Network.TON``).
- ``address`` must be a valid on-chain address for the network; invalid addresses will cause API errors.

Example
-------

.. code-block:: python

   from aiorocket2.enums import Network

   async with xRocketClient(api_key="KEY") as client:
       link = await client.get_withdrawal_link(currency="TON", network=Network.TON, address="EQ...", amount=0.1)
       print(link)

Common mistakes
---------------

- Passing ``network`` as a raw string instead of ``Network`` enum.
- Passing malformed address — check network-specific address format before calling.
