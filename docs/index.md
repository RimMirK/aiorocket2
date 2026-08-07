# aiorocket2 — Async xRocket Pay client

Welcome — these docs are written for developers embedding xRocket payments into Telegram bots and services.

This site contains:

- Quickstart and usage guides focused on common flows for Telegram integrations.
- A generated API reference (from docstrings) for every class and method in the client.
- Practical examples for the most-used methods: creating invoices, multi-cheques and withdrawal links.

If you open this documentation you should be able to implement payments with minimal time spent reading xRocket's upstream docs.

Explore:

- [Quickstart](quickstart.md)
- [API Reference](api/index.md)
- [Examples](examples.md)
- [Methods guide (practical)](guides/methods.md)

Why this docs set exists
------------------------

Many integrators only need a few methods. The goal here is to present those methods, their parameters (with explicit types and notes about enums), and short copy-pasteable examples so you can get working fast.

Important: where a parameter expects an Enum (see `aiorocket2.enums`) we emphasise that in examples. Passing arbitrary strings may be accepted by the library but can easily produce invalid API calls — treat enum fields as typed values.

Conventions used in examples
----------------------------

- Code examples are synchronous-friendly via `asyncio.run(...)` and assume Python 3.10+.
- All examples are in English; translations will be added later if the site engine supports it.
- API reference pages are auto-generated using `mkdocstrings`. If you want clearer method docs I will update docstrings in the source so the generated pages look great.

Next steps
----------

- Start at the [Quickstart](quickstart.md) to install and run a tiny working example.
- Then read the [Methods guide](guides/methods.md) for practical details on `create_invoice`, `create_multi_cheque`, and `get_withdrawal_link`.

If anything is unclear, open an issue on the repo or contact the maintainer listed in the footer.
