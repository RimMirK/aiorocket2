import aiorocket, asyncio
rocket = aiorocket.Rocket('dc5952421708c150b626f18b0')

async def main():
    print(f'API Version: {await rocket.version()}')
    print(f'App name: {(await rocket.info())["name"]}')
    print(f'Invoices: {[(v.id, v.link) for v in await rocket.get_invoices()]}')
    print(f'Cheques: {[(v.id, v.link) for v in await rocket.get_cheques()]}')
    print(f'Available currencies: {[{str(c): await c.get_price()} for c in await rocket.available_currencies()]}')
    print(f'Balances: {await rocket.balance()}')

asyncio.run(main())
