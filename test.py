import asyncio
from aiorocket import xRocketClient, Cheque, Invoice

with open(".api-key.txt", 'r') as f:
    API_KEY = f.read()

async def main():
    # Using async context manager for session
    async with xRocketClient(API_KEY, testnet=False) as client:

        # Get API info
        print(await client.get_info())


if __name__ == "__main__":
    asyncio.run(main())
