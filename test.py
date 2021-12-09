from typing import AsyncIterable
import autotrading.machine.upbit_machine as m
import asyncio


quo = m.QuotationAPI()
web = m.WebsocketAPI()
# get_market_code_test = quo.get_market_code(is_details=True)
# get_minute_candle_test = quo.get_minute_candle(to='2021-12-07 02:48:00', count=200)
# get_day_candle_test = quo.get_day_candle(market='BTC-ETH', to='2021-05-22 00:00:00', count=200, converting_price_unit='KRW')
# get_week_candle_test = quo.get_week_candle(to='2018-02-12 00:00:00', count=200)
# get_month_candle_test = quo.get_month_candle(count=200)
# get_orderbook_test = quo.get_orderbook(['KRW-BTC', 'KRW-ETH', 'KRW-SOL'])

# print(get_market_code_test)
# print(get_minute_candle_test)
# print(get_day_candle_test)
# print(get_week_candle_test)
# print(get_month_candle_test)
# print(get_orderbook_test)

# async def wss():
#     await web.subscribe_websocket()

# asyncio.run(wss())
type_field = [
    {"type":"trade","codes":["KRW-BTC"]},
    {"type":"orderbook","codes":["KRW-ETH"]},
    {"type":"ticker", "codes":["KRW-EOS"]}
]
web.set_subscribe_format(*type_field, ticket_field='UNIQUE_TICKET', format_field='SIMPLE')
asyncio.run(web.run_websocket())