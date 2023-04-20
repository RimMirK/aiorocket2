import aiohttp

class RocketAPIError(Exception):
    def __init__(self, data):
        self.message = data['message']
        self.errors = data.get('errors') or []
        super().__init__(self.message)

class Cheque:
    def __init__(self, api, id: int, currency: str, total: int, users: int, password: str, description: str, noitifications: bool, captcha: bool, telegramResources: list, refPercents: int, state: str, link: str, activations: int, refRewards: int, disabledLangs: list, forPremium: bool, forNewUsers: bool, linkedWallet: bool):
        self.id = id
        self.currency = currency
        self.total = total
        self.users = users
        self.password = password
        self.description = description
        self.noitifications = noitifications
        self.captcha = captcha
        self.telegramResources = telegramResources
        self.refPercents = refPercents
        self.state = state
        self.activations = activations
        self.refRewards = refRewards
        self.disabledLangs = disabledLangs
        self.forPremium = forPremium
        self.forNewUsers = forNewUsers
        self.linkedWallet = linkedWallet
        self.perUser = self.total / self.users
        self.api = api

    @classmethod
    def fromjson(cls, cheque, api):
        return cls(
            api,
            cheque.get('id'),
            cheque.get('currency'),
            cheque.get('total'),
            cheque.get('users'),
            cheque.get('password'),
            cheque.get('description'),
            cheque.get('sendNotifications'),
            cheque.get('captchaEnabled'),
            cheque.get('tgResources'),
            cheque.get('refProgramPercents'),
            cheque.get('state'),
            cheque.get('link'),
            cheque.get('activations'),
            cheque.get('refRewards'),
            cheque.get('disabledLanguages'),
            cheque.get('forPremium'),
            cheque.get('forNewUsersOnly'),
            cheque.get('linkedWallet')
        )
    async def delete(self):
        await self.api.delete_cheque(self.id)

class Invoice:
    def __init__(self, api, id: int, amount: int, totalPayments: int, paymentsLeft: int, description: str, hiddenMessage: str, payload: str, callbackUrl: str, currency: str, created: str, paid: str, status: str, expiredIn: int, link: str, payments: list):
        self.id = id
        self.amount = amount
        self.totalPayments = totalPayments
        self.paymentsLeft = paymentsLeft
        self.description = description
        self.hiddenMessage = hiddenMessage
        self.payload = payload
        self.callbackUrl = callbackUrl
        self.currency = currency
        self.created = created
        self.paid = paid
        self.expiredIn = expiredIn
        self.link = link
        self.payments = payments
        self.api = api

    @classmethod
    def fromjson(cls, invoice, api):
        return cls(
            api,
            invoice.get('id'),
            invoice.get('amount'),
            invoice.get('totalActivations'),
            invoice.get('activationsLeft'),
            invoice.get('description'),
            invoice.get('hiddenMessage'),
            invoice.get('payload'),
            invoice.get('callbackUrl'),
            invoice.get('currency'),
            invoice.get('created'),
            invoice.get('paid'),
            invoice.get('status'),
            invoice.get('expiredIn'),
            invoice.get('link'),
            invoice.get('payments')
        )
    async def delete(self):
        await self.api.delete_invoice(self.id)

class Currency:
    def __init__(self, currency: str, ticker: str, minTransfer: float, minCheque: float, minInvoice: float, minWithdraw: float, withdrawFee: float):
        self.currency = currency
        self.ticker = ticker
        self.minTransfer = minTransfer
        self.minCheque = minCheque
        self.minInvoice = minInvoice
        self.minWithdraw = minWithdraw
        self.withdrawFee = withdrawFee

    def __str__(self):
        return self.currency

    async def get_price(self, currency: str = 'RUB', fiat: bool = True):
        async with aiohttp.request('GET', f'https://trade.ton-rocket.com/rates/{"fiat" if fiat else "crypto"}/{self.currency}/{currency}') as r:
            r = await r.json()
            if not r['success']:
                raise RocketAPIError(r['message'])
        return r['data'].get('rate')
