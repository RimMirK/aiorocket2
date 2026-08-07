# create_multi_cheque — detailed

Signature
```
async def create_multi_cheque(self, currency: str, cheque_per_user: float, users_number: int, ref_program: int, password: str = None, description: str = None, send_notifications: bool = True, enable_captcha: bool = True, telegram_resources_ids: List[Union[int, str]] = None, for_premium: bool = False, linked_wallet: bool = False, disabled_languages: List[str] = None, enabled_countries: List[Country] = None) -> Cheque
```

Key notes
- `enabled_countries` — pass `Country` enum members (e.g., `[Country.US]`).
- `telegram_resources_ids` accepts mixed int/str resource ids.

Example
```python
from aiorocket2.enums import Country

async with xRocketClient(api_key="KEY") as client:
    chk = await client.create_multi_cheque(currency="TON", cheque_per_user=0.001, users_number=100, ref_program=0, enabled_countries=[Country.US, Country.GB])
    print(chk.id, chk.inviteUrl)
```

Common mistakes
- Supplying country codes as plain strings (typos). Use `Country` enum.
- Using too large `users_number` beyond API limits.
