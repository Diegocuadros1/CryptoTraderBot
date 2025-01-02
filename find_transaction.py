import os
import asyncio
import json

HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

async def find_transaction(wallet, slot):
    '''
        TODO
        Use the slot and run an RPC call to get the block data
        Transaction details.
        Participating wallets.
        Instructions executed in each transaction.
        
        use that data to identify the wallet that signed the transaction
        Determine its role (e.g., sender, receiver, or participant in a smart contract).
        find details on what the actions were preformed (e.g., token transfer, program execution)
        
        if the transaction was a token transfer, then get the token data
        
        print out exactly what the transaction did (e.g., token transfer, program execution)
        
        if the transaction was a token transfer, then get the token data and print it.

        Metadata: Includes token balances before and after the transaction.

    '''
    print("finding transaction", slot, wallet)

    transaction_url = f"https://rpc.helius.xyz/v0/addresses/{wallet}/transactions?api-key={HELIUS_API_KEY}&type=TRANSFER"


    #get block data
    info = await get_block_data(wallet, slot)
    pass