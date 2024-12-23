import time
import datetime
import asyncio
import os
import dotenv
import asyncio
import websockets
import json as JSON

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")
ws_url = f"wss://mainnet.helius-rpc.com/?api-key={API_KEY}"
rate_limit = asyncio.Semaphore(10) # Allow only 10 concurrent subscriptions per minute

# http_client = Client("https://api.mainnet-beta.solana.com")
    
async def subscribe(id, pubkey, websocket):
    subscription_payload = {
        "jsonrpc": "2.0",
        "id": id,
        "method": "accountSubscribe",
        "params": [
            pubkey,
            {
                "encoding": "jsonParsed"
            }
        ]
    }

    async with rate_limit:  
        await websocket.send(JSON.dumps(subscription_payload))
        await asyncio.sleep(6)  # 60 seconds / 10 requests


async def subscribe_to_wallets(wallets, websocket):
    tasks = []
    for idx, wallet in enumerate(wallets):
        tasks.append(subscribe(idx, wallet, websocket))
    await asyncio.gather(*tasks)


async def monitor_wallets(wallets):
    while True:
        try:
            async with websockets.connect(ws_url) as websocket:
                print("Connected to WebSocket.")
                await subscribe_to_wallets(wallets, websocket) # Subscribe to wallets with a certain rate limit

                while True:
                    message = await websocket.recv()
                    print("message: " + str(message))
                    print("Time: " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
      

        
async def main():

    #access wallets from txt file and add them to a list
    wallets = []
    print("Accessing wallets...")
    with open('./data/wallets.txt', 'r') as f:
        for line in f:
            try:
                print(line.strip())
                wallets.append(line.strip())
            except:
                print("error: " + line)
    
    if not wallets:
        print("No wallets found in the file. Exiting...")
        return
    try:
        await monitor_wallets(wallets)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    except Exception as e:
        print(f"Error in main: {e}")


asyncio.run(main())


    

