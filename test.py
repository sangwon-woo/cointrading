import websockets
import asyncio 
import json
import requests
import multiprocessing as mp
import pandas as pd
import time


url = "https://api.upbit.com/v1/market/all?isDetails=false"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

count = 0
ticker_list = []
for res in response.json():
    ticker = res['market']
    if ticker.startswith('KRW'):
        ticker_list.append(ticker)

df = pd.DataFrame()

async def upbit_ws_client():
    global df
    uri = "wss://api.upbit.com/websocket/v1"

    async with websockets.connect(uri) as websocket:
        subscribe_fmt = [ 
            {"ticket":"UNIQUE_TICKET"},
            # {
            #     "type": "ticker",
            #     "codes": ticker_list,
            #     "isOnlyRealtime": True
            # },
            {
                "type": "trade",
                "codes": ticker_list,
                "isOnlyRealtime": True
            },
            {
                "type": "orderbook",
                "codes": ticker_list,
                "isOnlyRealtime": True
            },
            {"format":"SIMPLE"}
        ]
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)
        
        a = 0
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            # df = df.append(data, ignore_index=True)
            # a += 1
            print(data)

async def main():
    await upbit_ws_client()

asyncio.run(main())
print(df)
