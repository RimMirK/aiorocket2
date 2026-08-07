Methods guide — practical usage
=================================

This page focuses on the most common methods for Telegram payment integrations.

.. contents::
   :local:

Overview
--------

- ``create_invoice(...)`` — create a single invoice (payable by a user).
- ``create_multi_cheque(...)`` — create a multi-cheque for many users.
- ``get_withdrawal_link(...)`` — generate a withdrawal link for on-chain withdraws.

General rules
-------------

- Where a parameter expects an ``Enum`` (see ``aiorocket2.enums``), pass the enum member (example: ``Network.TON``).
- Numeric amounts: the API uses high precision (up to 9 decimals). Use Python ``float`` for small scripts; consider ``decimal.Decimal`` for strict precision.
- Strings such as ``currency`` usually expect currency code (e.g. ``TON``). Use ``client.get_available_currencies()`` where possible.

create_invoice
--------------

Signature example (auto-generated)::

   async def create_invoice(self, currency: str, amount: float = None, min_payment: float = None, ... ) -> Invoice

What you need to know:

- ``currency`` (str): Currency code. Use ``client.get_available_currencies()`` to list valid currencies.
- ``amount`` (float): Optional. If provided the invoice has fixed amount.
- ``expired_in`` (int): Expiry in seconds, ``0`` — never expire.
- ``payload`` (str): Arbitrary opaque value returned in callbacks — useful to store your internal identifiers.

Example::

   async with xRocketClient(api_key="KEY") as client:
       inv = await client.create_invoice(currency="TON", amount=0.01, description="Donation")
       print(inv.id, inv.url)

create_multi_cheque
-------------------

Signature example::

   async def create_multi_cheque(self, currency: str, cheque_per_user: float, users_number: int, ref_program: int, ... ) -> Cheque

Key parameters:

- ``cheque_per_user`` (float): Amount per user, up to 9 decimal places.
- ``users_number`` (int): Number of activations users can take.
- ``enabled_countries`` (List[Country]): Prefer passing ``Country`` enum members (e.g., ``[Country.RU, Country.US]``).

Example::

   from aiorocket2 import xRocketClient
   from aiorocket2.enums import Country

   async with xRocketClient(api_key="KEY") as client:
       chk = await client.create_multi_cheque(currency="TON", cheque_per_user=0.001, users_number=50, ref_program=0, enabled_countries=[Country.US, Country.GB])
       print(chk.id, chk.inviteUrl)

get_withdrawal_link
-------------------

Signature example::

   async def get_withdrawal_link(self, currency: str, network: Network, address: str, amount: float = 0, ...) -> Optional[str]

Notes:

- ``network`` should be a ``Network`` enum member (e.g., ``Network.TON``).
- The method returns a Telegram app link (string) or raises ``xRocketAPIError`` on failure.

Example::

   from aiorocket2.enums import Network

   async with xRocketClient(api_key="KEY") as client:
       link = await client.get_withdrawal_link(currency="TON", network=Network.TON, address="EQ...", amount=0.05)
       print(link)

Next steps
----------

- Browse the auto-generated :doc:`/api/index` for full signatures and model descriptions.
- I will update docstrings where needed so those pages include more examples and parameter notes.
