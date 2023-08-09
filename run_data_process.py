
import os
import datetime
import time
from autotrading.data.collector import UpbitCollector
from autotrading.data.collect import collect_data_with_multiprocess
from autotrading.data.backup import backup_start
from autotrading.machine.upbit_machine import QuotationAPI
from config.setting import *
from util.util import time_print
# schedule 모듈 사용하기

upbit_minutely_files = os.listdir(DIR_UPBIT_MINUTELY_CANDLE)
upbit_daily_files = os.listdir(DIR_UPBIT_DAILY_CANDLE)

if __name__ == '__main__':
    collector = UpbitCollector(QuotationAPI)
    last_hour = 0

    while True:
        market_code_in_upbit = collector.get_market_code()
        minutely_market_code_i_have = [m[:-4]
                                       for m in upbit_minutely_files if m.endswith('arr')]
        daily_market_code_i_have = [m[:-4]
                                    for m in upbit_daily_files if m.endswith('arr')]

        if set(market_code_in_upbit) != set(minutely_market_code_i_have):
            print('업비트 종목들과 저장된 종목들이 서로 다름')
            new_code = set(market_code_in_upbit) - \
                set(minutely_market_code_i_have)
            delete_code = set(minutely_market_code_i_have) - \
                set(market_code_in_upbit)

            if new_code:
                collector.collect_minutely_all_data(list(new_code))
                pass
            if delete_code:
                # TODO :상폐된 종목 백업하는 메소드 만들기
                pass

        now = datetime.datetime.now()

        # 1시간 마다 1분봉 다운받기
        print('1분봉 업데이트 전 현재 시간:', now)
        if now.hour != last_hour and now.minute == 0 and (0 <= now.second < 10):
            s = time.time()
            print('1분봉 업데이트 시작 시간:', now)
            time.sleep(1)
            collect_data_with_multiprocess(
                'minutely', collector, minutely_market_code_i_have, 9)
            last_hour = now.hour
            print(f'{now} => 1분봉 업데이트 완료')
            print('1분봉 소요시간', end=' ')
            time_print(s, time.time())

        if now.hour == 9:
            # 매일 오전 9시 30분에 일봉데이터 다운받기
            while True:
                now = datetime.datetime.now()
                print('일봉 업데이트 전 현재 시간:', now)
                if now.hour == 9 and now.minute == 30 and (0 <= now.second < 10):
                    s = time.time()
                    print('일봉 업데이트 시작 시간:', now)
                    time.sleep(1)
                    collect_data_with_multiprocess(
                        'daily', collector, daily_market_code_i_have, 3)
                    print(f'{now} => 일봉 업데이트 완료')
                    print('일봉 소요시간', end=' ')
                    time_print(s, time.time())

                    # 이후 데이터 백업하기
                    backup_start(DIR_UPBIT_DAILY_CANDLE,
                                 DIR_UPBIT_DAILY_CANDLE_BACKUP, '.arr')
                    backup_start(DIR_UPBIT_MINUTELY_CANDLE,
                                 DIR_UPBIT_MINUTELY_CANDLE_BACKUP, '.arr')

                    break

                elif now.hour == 9 and now.minute < 30:
                    delta = 1800 - ((now.minute * 60) + now.second) + 1
                    print(f'일봉 데이터 업데이트 전 {delta}초 동안 잠자기')
                    time.sleep(delta)

        now = datetime.datetime.now()
        delta = 3600 - ((now.minute * 60) + now.second) + 1
        print(f'1분봉 데이터 업데이트 전 {delta}초 동안 잠자기')
        time.sleep(delta)
