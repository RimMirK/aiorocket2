import aiorocket, asyncio
rocket = aiorocket.Rocket('412762fa70728f971f90719ad', testnet=True)

async def main():
    print(f'API Version: {await rocket.version()}')
    print(f'App name: {(await rocket.info())["name"]}')
    inv = await rocket.create_invoice(
        amount=0.123,
        description="покупка лучшой вещи в мире",
        hiddenMessage="спасибо",
        callbackUrl="https://t.me/Duo_sova", # опять мой реальный ТГ
        payload="some payload",
        expiredIn=60
    )
    print(f'New invoice: {inv.amount} {inv.currency} | {inv.id} | {inv.link}')
    print(f'Invoices: {[(v.id, v.link) for v in await rocket.get_invoices()]}')
    for inv in await rocket.get_invoices():
        print(f'Deleting {inv.id} ...')
        await inv.delete() # удобное удаление через ООП
    print(f'Cheques: {[(v.id, v.link) for v in await rocket.get_cheques()]}')
    print(f'Available currencies: {[{str(c): await c.get_price()} for c in await rocket.available_currencies()]}')
    print(f'Balances: {await rocket.balance()}')

asyncio.run(main())
