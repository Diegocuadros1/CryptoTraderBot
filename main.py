import time
import datetime
import asyncio
import os
import asyncio
import websockets
import json as JSON
from find_transaction import find_transaction


ws_url = "wss://rpc-proxy.cuadrosda21.workers.dev"
rate_limit = asyncio.Semaphore(10) # Allow only 10 concurrent subscriptions per minute
 
    
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

async def send_pings(websocket):
    """Send periodic pings to keep the connection alive."""
    while True:
        try:
            await websocket.ping()
            print(f"Ping sent at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            await asyncio.sleep(60)  # Send ping every 20 seconds
        except Exception as e:
            print(f"Error sending ping: {e}")
            break

async def get_block_data(wallet, slot):
    
    print("getting block data", wallet, slot)
    pass

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

                ping_task = asyncio.create_task(send_pings(websocket))

                await subscribe_to_wallets(wallets, websocket) # Subscribe to wallets with a certain rate limit

                results = {}
                while True:
                    message = await websocket.recv()
                    message = JSON.loads(message)
                    print("Time: " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

                    #if the account is an notification, then find the transaction with wallet & sub id
                    if "method" in message:
                        print("ACCOUNT NOTIFICATION", message)
                        slot = message["params"]["result"]["context"]["slot"]
                        wallet = results[message["params"]["subscription"]]
                        find_transaction(wallet, slot)

                    #if the account is a subscription, then match each wallet with the subscription id
                    else:
                        results[message["result"]] = wallets[message["id"]]
                        print("Wallet", wallets[message["id"]], " subscribed. subscription id result: ", message["result"])

                

        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}. Retrying in 5 seconds...")
            print("Time: " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
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


    

