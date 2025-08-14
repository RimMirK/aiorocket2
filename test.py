import asyncio
import json
import shutil
from aiorocket import *

with open(".api-key.txt", 'r') as f:
    API_KEY = f.read()

def hr():
    width = shutil.get_terminal_size(fallback=(80, 20)).columns
    print('-' * width)



    


async def main():
    # Using async context manager for session
    async with xRocketClient(API_KEY, testnet=True) as client:

        print("TESTING")

        hr()

        # Get API info
        info = await client.get_info()
        print("App info:")
        print(f"  name: {info.name!r}")
        print(f"  balances:")
        for balance in info.balances:
            print(f"    {balance.currency}: {balance.balance}")

        hr()

        try:
            tr_id = generate_idempotency_id()
            # transfer = await client.send_transfer(
            #     tg_user_id=466040514,
            #     currency='USDT',
            #     amount=1,
            #     transfer_id=tr_id
            # )
            # print(f"generated invoice with transfer_id = {tr_id!r}")
            # print(f"Transfer: {transfer}")
        except xRocketAPIError as e:
            errors = e.payload.get('errors', [])
            if not errors:
                raise
            for error in errors:
            
                if error['property'] == 'amount' and \
                    "is more than app balance" in error['error']:
                    print(f"Can't send transfer because of low balance: {error['error']}")
                    break
            else:
                raise
        
        hr()

        try:
            # withdrawal = await client.create_withdrawal(
            #     network=Network.TON,
            #     address="UQDJPTzJOo78ipLSu-7GstaqXFoXAVr0DUAk6UW-53wpgvB1",
            #     currency="USDT",
            #     amount=1,
            #     withdrawal_id=gii(),
            #     comment='hi'
            # )
            # print(f'Created withdrawal: {withdrawal}')
            pass
        except xRocketAPIError as e:
            print("withdrawal has not been created", e)

        hr()
        
        # withdrawal = await client.get_withdrawal('1755115621.4672675')
        # print(f"Withdrawal info: {withdrawal}")

        hr()

        fees = await client.get_withdrawal_fees()
        print(f"All withdrawal fees:")
        for fee in fees:
            print(f"  code: {fee.code}")
            print(f"  min withdrawal: {fee.min_withdrawal}")
            print(f"  fees:")
            for f in fee.fees:
                print(f"    currency: {f.currency}")
                print(f"    fee: {f.fee}")

        hr()

        # cheque = await client.create_multi_cheque(
        #     currency="DHD",
        #     cheque_per_user=7,
        #     users_number=1,
        #     ref_program=0,
        #     description="hi"
        # )
        # print("Created cheque:", cheque)
        
        hr()
        
        cheques = await client.get_multi_cheques()
        print(f"Cheques: {cheques}")
        
        # hr()
        
        # cheque = await client.get_multi_cheque(426842)
        # print(f"Cheque: {cheque}")
        
        hr()
        
        invoice = await client.create_invoice(
            1, 0, 1, "USDT", "oplatite", "spasibo", True, payload="test payload"
        )
        print(f"Invoice: {invoice}")
        
        hr()
        
        invoices = await client.get_invoices(limit=3)
        print(f"Invoices: {dict(invoices)}")
        print(invoices.results[0].created)
        print(invoices.results[0].created.datetime)
        print(invoices.results[0].created.timestamp)
        print(invoices.results[0].paid.datetime)
        print(invoices.results[0].paid.timestamp)
    


if __name__ == "__main__":
    asyncio.run(main())
