#  aiorocket2 - Asynchronous Python client for xRocket Pay API
#  Copyright (C) 2025-present RimMirK
#
#  This file is part of aiorocket2.
#
#  aiorocket2 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3 of the License.
#
#  aiorocket2 is an independent, unofficial client library.
#  It is a near one-to-one reflection of the xRocket Pay API:
#  all methods, parameters, objects and enums are implemented.
#  If something does not work as expected, please open an issue.
#
#  You should have received a copy of the GNU General Public License
#  along with aiorocket2.  If not, see the LICENSE file.
#
#  Repository: https://github.com/RimMirK/aiorocket2
#  Documentation: https://aiorocket2.rimmirk.pp.ua
#  Telegram: @RimMirK



"""
This file is a developer test file, used to experiment and test the library
during development. It is not part of the official release
"""

import asyncio
import json
import shutil
from aiorocket2 import *

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

        fees = await client.get_withdrawal_fees(currency="TONCOIN")
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
        
        hr()
        
        # # cheque = await client.get_multi_cheque(10)
        # # print(f"Cheque: {cheque}")
        
        # hr()
        
        # # cheque = await client.edit_multi_cheque(cheque_id=cheque.id, description='edited', password='hehe')
        # # print(f"Edited cheque: {cheque}")
        
        # # return
        # hr()
        
        # deleted = await client.delete_multi_cheque(cheque_id=cheque.id)
        # print(f"Deleted cheque: {deleted!r}")
        
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
        
        hr()
        
        # pokachto vse rabotajet, ura
        
        # invoice = await client.get_invoice(209)
        # print(f"Get invoice: {dict(invoice)}")
        
        # hr()
        
        # deleted = await client.delete_invoice(209)
        # print(f"deleted invoice: {deleted}")
        
        hr()
        
        # idk what this method really do, at testnet it doesn't work 
        link = await client.get_withdrawal_link(
            "USDT", Network.TON, "UQDJPTzJOo78ipLSu-7GstaqXFoXAVr0DUAk6UW-53wpgvB1",
            2, comment='test comment'
        )
        print(f"Withdrawal link: {link!r}")
        
        hr()
        
        alive = await client.check_health()
        print(f"alive: {alive}")
        
        hr()
        
        currencies = await client.get_available_currencies()
        print(f"Currencies: {currencies}")
        print(f"Currencies dict: {(currencies[0]).as_dict()}")
        
        
    


if __name__ == "__main__":
    asyncio.run(main())
