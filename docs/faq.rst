FAQ
===

Q: The client accepts strings where the API expects enums — is that safe?

A: The library may accept plain strings in some places, but you should prefer passing enum members from ``aiorocket2.enums`` (for example ``Network.TON`` or ``Country.US``). This protects against typos and keeps your code self-documenting.

Q: I get `xRocketAPIError` with a non-helpful message — how to debug?

A: Inspect the exception payload; enable logging of request/response in your environment. Verify you pass correct types and valid values (enums, currency codes, correct numeric precision). For transient network errors, the client will retry according to configured `retries` and `backoff_base`.

Q: How to use testnet?

A: Initialize the client with ``testnet=True`` or set ``base_url`` to your staging endpoint. Testnet avoids real transfers.

Q: Where to find upstream API docs?

A: Official xRocket API: https://pay.xrocket.exchange/api
