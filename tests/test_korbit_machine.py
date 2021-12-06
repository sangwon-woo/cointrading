import websockets
import asyncio 
import json
import requests
import multiprocessing as mp
import pandas as pd
import time

async def korbit_ws_client():
    uri = "wss://ws.korbit.co.kr/v1/user/push"

    async with websockets.connect(uri) as websocket:
        subscribe_fmt = {
            "accessToken":"o4vMmtqOUVMgVVndi5li3w6Y1eh7Z5qxadSO429WUplGXkDHmJivlbt3SvXvy",
            "timestamp":int(time.time()),
            "event":"korbit:subscribe",
            "data":{
                # "channels":[
                #     "ticker:btc_krw",
                #     "orderbook:btc_krw",
                #     "transaction:btc_krw"
                # ]
                "channels":["ticker"]
            }
        }
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
    await korbit_ws_client()

asyncio.run(main())
