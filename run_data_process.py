
import os
import multiprocessing as mp
import random
import datetime
import pandas as pd
from autotrading.data.collector import UpbitCollector
from autotrading.machine.upbit_machine import QuotationAPI
from config.setting import *


upbit_minutely_files = os.listdir(DIR_UPBIT_MINUTELY_CANDLE)
upbit_daily_files = os.listdir(DIR_UPBIT_DAILY_CANDLE)

if __name__ == '__main__':
    collector = UpbitCollector(QuotationAPI)

    while True:
        krw_market_code = collector.get_market_code()
        existing_market = [m[:-4]
                           for m in upbit_minutely_files if m.endswith('arr')]
        random.shuffle(existing_market)

        if set(krw_market_code) != set(existing_market):
            print('시장 코드가 다름')
            # 상장 종목은 데이터를 다운 받고
            # 상폐 종목은 데이터를 백업한다.

        first_idx = len(existing_market) // 3
        second_idx = first_idx * 2

        first_market = existing_market[:first_idx]
        second_market = existing_market[first_idx:second_idx]
        third_market = existing_market[second_idx:]

        processes = []

        proc1 = mp.Process(
            target=collector.collect_minutely_data_until_now, args=(first_market,))
        proc2 = mp.Process(
            target=collector.collect_minutely_data_until_now, args=(second_market,))
        proc3 = mp.Process(
            target=collector.collect_minutely_data_until_now, args=(third_market,))

        processes.append(proc1)
        processes.append(proc2)
        processes.append(proc3)

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        # time.sleep(3600)
        break

    existing_market = [m[:-4] for m in upbit_daily_files if m.endswith('arr')]
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

    proc1 = mp.Process(
        target=collector.collect_daily_data_until_now, args=(first_market,))
    proc2 = mp.Process(
        target=collector.collect_daily_data_until_now, args=(second_market,))
    proc3 = mp.Process(
        target=collector.collect_daily_data_until_now, args=(third_market,))

    processes.append(proc1)
    processes.append(proc2)
    processes.append(proc3)

    for p in processes:
        p.start()

    for p in processes:
        p.join()
