from autotrading.data.collector import Collector
import autotrading.machine.upbit_machine as m
import os
import multiprocessing as mp
import random
import time


class UpbitAPIException(Exception):
    pass

type_field = [
    {"type":"trade","codes":["KRW-BTC"]},
    # {"type":"orderbook","codes":["KRW-ETH"]},
    # {"type":"ticker", "codes":["KRW-EOS"]}
]



minutely = os.listdir('D:\\coin_database\\domestic\\upbit\\minutely')
daily = os.listdir('D:\\coin_database\\domestic\\upbit\\daily')

if __name__ == '__main__':
    while True:

        collector = Collector(m.QuotationAPI)
        krw_market_code = collector.get_market_code()

        existing_market = [m[:-4] for m in minutely if m.endswith('arr')]
        random.shuffle(existing_market)

        if set(krw_market_code) != set(existing_market):
            print('시장 코드가 다름')
            exit()

        first_idx = len(existing_market) // 3
        second_idx = first_idx * 2

        first_market = existing_market[:first_idx]
        second_market = existing_market[first_idx:second_idx]
        third_market = existing_market[second_idx:]

        processes = []

        proc1 = mp.Process(target=collector.collect_minutely_data_until_now, args=(first_market,))
        proc2 = mp.Process(target=collector.collect_minutely_data_until_now, args=(second_market,))
        proc3 = mp.Process(target=collector.collect_minutely_data_until_now, args=(third_market,))

        processes.append(proc1)
        processes.append(proc2)
        processes.append(proc3)

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        # time.sleep(3600)
        break

    existing_market = [m[:-4] for m in daily if m.endswith('arr')]
    random.shuffle(existing_market)

    if set(krw_market_code) != set(existing_market):
        print('시장 코드가 다름')
        exit()

    first_idx = len(existing_market) // 3
    second_idx = first_idx * 2

    first_market = existing_market[:first_idx]
    second_market = existing_market[first_idx:second_idx]
    third_market = existing_market[second_idx:]

    processes = []

    proc1 = mp.Process(target=collector.collect_daily_data_until_now, args=(first_market,))
    proc2 = mp.Process(target=collector.collect_daily_data_until_now, args=(second_market,))
    proc3 = mp.Process(target=collector.collect_daily_data_until_now, args=(third_market,))

    processes.append(proc1)
    processes.append(proc2)
    processes.append(proc3)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    

        