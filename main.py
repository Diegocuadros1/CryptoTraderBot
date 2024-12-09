from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solana.rpc.websocket_api import connect
from solana.rpc.async_api import AsyncClient
import datetime
import asyncio


http_client = Client("https://api.mainnet-beta.solana.com")

async def monitor_wallets(wallets):
    async with connect("wss://api.mainnet-beta.solana.com") as websocket:
        subscriptions = {}

        for wallet in wallets:
            try:
                await websocket.account_subscribe(wallet, encoding="jsonParsed") 
            except Exception as e:
                print(f"Error subscribing to account: {wallet}. Error: {e}")
                continue

        while True:
            try:
                message = await websocket.recv()
                print("message: " + str(message))                

            except Exception as e:
                print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Error: {e}")
                break
async def main():

    #access wallets from txt file and add them to a list
    wallets = []
    print("Accessing wallets...")
    with open('./data/wallets.txt', 'r') as f:
        for line in f:
            try:
                wallets.append(Pubkey.from_string(line.strip()))
            except:
                print("incorrect wallet accessed: " + line)
        
    await monitor_wallets(wallets)


asyncio.run(main())


    

