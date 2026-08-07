create_invoice — detailed
========================

Signature
---------

.. code-block:: python

   async def create_invoice(self, currency: str, amount: float = None, min_payment: float = None, num_payments: int = 1, description: str = None, hidden_message: str = None, comments_enabled: bool = False, callback_url: str = None, payload: str = None, expired_in: int = 0, platform_id: str = None) -> Invoice

Parameters (practical)
----------------------

- ``currency`` (str): Currency code, e.g. ``"TON"``. Use ``client.get_available_currencies()``.
- ``amount`` (float | None): Fixed amount for the invoice. Use decimals up to 9 places.
- ``min_payment`` (float | None): Minimum payment when ``amount`` is not provided.
- ``num_payments`` (int): Number of allowed partial payments (default 1).
- ``description`` (str): Visible description for the payer (max 1000 chars).
- ``hidden_message`` (str): Message shown after successful payment (max 2000 chars).
- ``comments_enabled`` (bool): Allow comments on invoice.
- ``callback_url`` (str): Optional callback URL for merchant return.
- ``payload`` (str): Opaque string returned in callbacks — store your internal id here.
- ``expired_in`` (int): Expiry time in seconds (0 — never expire).

Example
-------

.. code-block:: python

   async with xRocketClient(api_key="KEY") as client:
       inv = await client.create_invoice(currency="TON", amount=0.005, description="Tip")
       print(inv.id, inv.url)

Common mistakes
---------------

- Passing non-existent currency codes — call ``get_available_currencies()``.
- Using floats without awareness of precision — for accounting-sensitive flows prefer ``decimal.Decimal``.
- Assuming synchronous behaviour — remember methods are ``async``.
