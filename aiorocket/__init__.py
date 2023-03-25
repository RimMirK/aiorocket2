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

    async def version(self):
        async with aiohttp.request('GET', f'{self.BASE_URL}/version') as r:
            return (await r.json()).get('version')

    async def info(self):
        async with aiohttp.request('GET', f'{self.BASE_URL}/app/info', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            return {'name': r['data']['name'], 'feePercents': r['data']['feePercents']}

    async def balance(self, only_positive=True):
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

    async def send(self, **params):
        async with aiohttp.request('POST', f'{self.BASE_URL}/app/transfer', json=params, headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            return r['data']['id']

    async def withdraw(self, **params):
        async with aiohttp.request('POST', f'{self.BASE_URL}/app/withdrawal', json=params, headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            return r['data']['id']

    async def create_cheque(self, **params):
        async with aiohttp.request('POST', f'{self.BASE_URL}/multi-cheques', json=params, headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            cheque = r['data']
        return Cheque.fromjson(cheque)

    async def get_cheques(self, limit: int = 100, offset: int = 0):
        async with aiohttp.request('GET', f'{self.BASE_URL}/multi-cheques', params={'limit': limit, 'offset': offset}, headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            r = r['data']
        result = []
        for cheque in r['results']:
            result.append(Cheque.fromjson(cheque))
        return result

    async def get_cheque(self, id: int):
        async with aiohttp.request('GET', f'{self.BASE_URL}/multi-cheques/{id}', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            cheque = r['data']
        return Cheque.fromjson(cheque)

    async def edit_cheque(self, id: int, **params):
        async with aiohttp.request('PUT', f'{self.BASE_URL}/multi-cheques/{id}', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            return Cheque.fromjson(r)

    async def delete_cheque(self, id: int):
        async with aiohttp.request('DELETE', f'{self.BASE_URL}/multi-cheques/{id}', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])

    async def create_invoice(self, **params):
        async with aiohttp.request('POST', f'{self.BASE_URL}/tg-invoices', json=params, headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            r = r['data']
        return Invoice.fromjson(r)

    async def get_invoices(self, limit: int = 100, offset: int = 0):
        async with aiohttp.request('GET', f'{self.BASE_URL}/tg-invoices', params={'limit': limit, 'offset': offset}, headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            r = r['data']
        result = []
        for invoice in r['results']:
            result.append(Invoice.fromjson(invoice))
        return result

    async def get_invoice(self, id: int):
        async with aiohttp.request('GET', f'{self.BASE_URL}/tg-invoices/{id}', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
            invoice = r['data']
        return Invoice.fromjson(invoice)

    async def delete_cheque(self, id: int):
        async with aiohttp.request('DELETE', f'{self.BASE_URL}/tg-invoices/{id}', headers=self._headers) as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])

    async def available_currencies(self):
        async with aiohttp.request('GET', f'{self.BASE_URL}/currencies/available') as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
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