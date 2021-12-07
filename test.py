import autotrading.machine.upbit_machine as m

quo = m.QuotationAPI()
# get_market_code_test = quo.get_market_code(is_details=True)
# get_minute_candle_test = quo.get_minute_candle(to='2021-12-07 02:48:00', count=200)
# get_day_candle_test = quo.get_day_candle(market='BTC-ETH', to='2021-05-22 00:00:00', count=200, converting_price_unit='KRW')
get_week_candle_test = quo.get_week_candle(to='2018-02-12 00:00:00', count=200)

# print(get_market_code_test)
# print(get_minute_candle_test)
# print(get_day_candle_test)
print(get_week_candle_test)