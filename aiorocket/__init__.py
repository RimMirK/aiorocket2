import aiohttp, asyncio
from .classes import *
from async_property import async_property

BASEURL_MAINNET = 'https://pay.ton-rocket.com'
BASEURL_TESTNET = 'https://dev-pay.ton-rocket.com'

class Rocket:
    def __init__(self, api_key: str, testnet=False):
        self.BASE_URL = BASEURL_TESTNET if testnet else BASEURL_MAINNET
        self.api_key = api_key
        self._headers = {'Rocket-Pay-Key': self.api_key}

    async def version(self) -> str:
        async with aiohttp.request('GET', f'{self.BASE_URL}/version') as r:
            return (await r.json())['version']

    async def info(self) -> dict:
        async with aiohttp.request('GET', f'{self.BASE_URL}/app/info', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            return {'name': r['data']['name'], 'feePercents': r['data']['feePercents']}

    async def balance(self, only_positive: bool = True) -> dict:
        async with aiohttp.request('GET', f'{self.BASE_URL}/app/info', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            result = {}
            for pair in r['data']['balances']:
                if only_positive and not pair['balance']:
                    continue
                result[pair['currency']] = pair['balance']
            return result

    async def _post_request(self, endpoint: str, params: dict) -> dict:
        async with aiohttp.request('POST', f'{self.BASE_URL}/{endpoint}', json=params, headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r)
            return r['data']

    async def send(self, **params) -> int:
        return await self._post_request('app/transfer', params)['id']

    async def withdraw(self, **params) -> int:
        return await self._post_request('app/withdrawal', params)['id']

    async def create_cheque(self, **params) -> Cheque:
        return Cheque.fromjson(await self._post_request('multi-cheques', params), self)

    async def get_cheques(self, limit: int = 100, offset: int = 0) -> list:
        async with aiohttp.request('GET', f'{self.BASE_URL}/multi-cheques', params={'limit': limit, 'offset': offset}, headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r)
            return [await Cheque.fromjson(cheque, self) for cheque in r['data']['results']]

    async def get_cheque(self, id: int) -> Cheque:
        async with aiohttp.request('GET', f'{self.BASE_URL}/multi-cheques/{id}', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r)
            return Cheque.fromjson(r['data'], self)

    async def edit_cheque(self, id: int, **params) -> Cheque:
        async with aiohttp.request('PUT', f'{self.BASE_URL}/multi-cheques/{id}', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r)
            return Cheque.fromjson(r, self)

    async def delete_cheque(self, id: int) -> None:
        async with aiohttp.request('DELETE', f'{self.BASE_URL}/multi-cheques/{id}', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r)

    async def create_invoice(self, **params) -> Invoice:
        return Invoice.fromjson(await self._post_request('tg-invoices', params), self)

    async def get_invoices(self, limit: int = 100, offset: int = 0) -> list:
        async with aiohttp.request('GET', f'{self.BASE_URL}/tg-invoices', params={'limit': limit, 'offset': offset}, headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r)
            r = r['data']
        result = []
        for invoice in r['results']:
            result.append(Invoice.fromjson(invoice, self))
        return result

    async def get_invoice(self, id: int) -> Invoice:
        async with aiohttp.request('GET', f'{self.BASE_URL}/tg-invoices/{id}', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r)
            invoice = r['data']
        return Invoice.fromjson(invoice, self)

    async def delete_invoice(self, id: int) -> None:
        async with aiohttp.request('DELETE', f'{self.BASE_URL}/tg-invoices/{id}', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r)

    async def available_currencies(self) -> list:
        async with aiohttp.request('GET', f'{self.BASE_URL}/currencies/available') as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r)
        results = []
        for currency in r['data']['results']:
            results.append(Currency(
                currency.get('currency'),
                currency.get('name'),
                currency.get('minTransfer'),
                currency.get('minCheque'),
                currency.get('minInvoice'),
                currency.get('minWithdraw'),
                currency.get('feeWithdraw')
            ))
        return results
