import time
import pandas as pd
from config.setting import *

class Collector:
    def __init__(self, machine):
        self.machine = machine()

    def get_last_time(self, df):
        last_time = df.loc[df.shape[0]-1, 'candle_date_time_utc']
        last_time = ' '.join(last_time.split('T'))

        return last_time
        
    def get_market_code(self):
        market = self.machine.get_market_code()
        krw_market_code = [c for c in market['market'].to_list() if c.startswith('KRW')]

        return krw_market_code

    def collect_minutely_all_data(self, markets:list):
        
        for market in markets:
            s = time.time()
            coin_df = pd.DataFrame()
            save_dir = UPBIT_DATABASE_DIR + f'\\minutely\\{market}.csv'
            latest_df = self.machine.get_minute_candle(unit=1, market=market, count=200)

            last_time = self.get_last_time(latest_df)
            coin_df = coin_df.append(latest_df, ignore_index=True)
            
            while True:
                df = self.machine.get_minute_candle(unit=1, market=market, to=last_time, count=200)
                if len(df.index) == 0:
                    break
                last_time = self.get_last_time(df)
                coin_df = coin_df.append(df, ignore_index=True)

            coin_df.to_csv(save_dir, index=None, encoding='utf-8')
            print(f'{market} => Delta', time.time() - s)

    def collect_minutely_data_until_now(self, markets:list):

        for market in markets:
            s = time.time()
            load_dir = UPBIT_DATABASE_DIR + f'\\minutely\\{market}.csv'
            save_dir = UPBIT_DATABASE_DIR + f'\\minutely\\{market}.csv'

            old_df = pd.read_csv(load_dir, encoding='utf-8')
            first_time = old_df.loc[0, 'candle_date_time_utc']

            latest_df = self.machine.get_minute_candle(unit=1, market=market, count=200)
            last_time = self.get_last_time(latest_df)
            
            if last_time <= first_time:
                subset_df = latest_df[latest_df['candle_date_time_utc'] > first_time]
                old_df = old_df.append(subset_df, ignore_index=True)

                return old_df
            else:
                while True:
                    df = self.machine.get_minute_candle(unit=1, market=market, to=last_time)

                    if last_time <= first_time:
                        subset_df = df[df['candle_date_time_utc'] > first_time]
                        old_df = old_df.append(subset_df, ignore_index=True)
                        return old_df
                    last_time = self.get_last_time(df)
                    old_df = old_df.append(df, ignore_index=True)

    def collect_daily_all_data(self, markets:list):
        
        for market in markets:
            s = time.time()
            coin_df = pd.DataFrame()
            save_dir = UPBIT_DATABASE_DIR + f'\\daily\\{market}.csv'
            latest_df = self.machine.get_minute_candle(unit=1, market=market, count=200)

            last_time = self.get_last_time(latest_df)
            coin_df = coin_df.append(latest_df, ignore_index=True)
            
            while True:
                df = self.machine.get_minute_candle(unit=1, market=market, to=last_time, count=200)
                if len(df.index) == 0:
                    break
                last_time = self.get_last_time(df)
                coin_df = coin_df.append(df, ignore_index=True)

            coin_df.to_csv(save_dir, index=None, encoding='utf-8')
            print(f'{market} => Delta', time.time() - s)

    def collect_daily_data_until_now(self, markets:list):

        for market in markets:
            s = time.time()
            load_dir = UPBIT_DATABASE_DIR + f'\\daily\\{market}.csv'
            save_dir = UPBIT_DATABASE_DIR + f'\\daily\\{market}.csv'

            old_df = pd.read_csv(load_dir, encoding='utf-8')
            first_time = old_df.loc[0, 'candle_date_time_utc']

            latest_df = self.machine.get_minute_candle(unit=1, market=market, count=200)
            last_time = self.get_last_time(latest_df)
            
            if last_time <= first_time:
                subset_df = latest_df[latest_df['candle_date_time_utc'] > first_time]
                old_df = old_df.append(subset_df, ignore_index=True)

                return old_df
            else:
                while True:
                    df = self.machine.get_minute_candle(unit=1, market=market, to=last_time)

                    if last_time <= first_time:
                        subset_df = df[df['candle_date_time_utc'] > first_time]
                        old_df = old_df.append(subset_df, ignore_index=True)
                        return old_df
                    last_time = self.get_last_time(df)
                    old_df = old_df.append(df, ignore_index=True)                

