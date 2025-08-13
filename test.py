import asyncio
from aiorocket import xRocketClient, Cheque, Invoice

API_KEY = "7a26b4dafc47f0d7869c67d52"

async def main():
    # Using async context manager for session
    async with xRocketClient(API_KEY, testnet=False) as client:

        # Get API info
        print(await client.get_info())


if __name__ == "__main__":
    asyncio.run(main())
