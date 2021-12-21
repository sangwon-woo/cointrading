import time
import pandas as pd
import numpy as np
from config.setting import *
from dateutil.parser import parse

class Collector:
    def __init__(self, machine):
        self.machine = machine()

    def check_dtypes(self, df):
        col_dtypes = {}
        for col in df.columns:
            dtype = df[col].dtype

            if dtype == 'int' or dtype == 'float':
                c_min = df[col].min()
                c_max = df[col].max()
            elif dtype == 'object':
                n_unique = df[col].nunique()
                threshold = n_unique / df.shape[0]

            if dtype == 'int':
                if c_min >= np.iinfo(np.int8).min and c_max <= np.iinfo(np.int8).max:
                    col_dtype = 'int8'
                elif c_min >= np.iinfo(np.uint8).min and c_max <= np.iinfo(np.uint8).max:
                    col_dtype = 'uint8'
                elif c_min >= np.iinfo(np.int16).min and c_max <= np.iinfo(np.int16).max:
                    col_dtype = 'int16'
                elif c_min >= np.iinfo(np.uint16).min and c_max <= np.iinfo(np.uint16).max:
                    col_dtype = 'uint16'
                elif c_min >= np.iinfo(np.int32).min and c_max <= np.iinfo(np.int32).max:
                    col_dtype = 'int32'
                elif c_min >= np.iinfo(np.uint32).min and c_max <= np.iinfo(np.uint32).max:
                    col_dtype = 'uint32'
                elif c_min >= np.iinfo(np.int64).min and c_max <= np.iinfo(np.int64).max:
                    col_dtype = 'int64'
                elif c_min >= np.iinfo(np.uint64).min and c_max <= np.iinfo(np.uint64).max:
                    col_dtype = 'uint64'
                elif c_min >= np.iinfo(np.int128).min and c_max <= np.iinfo(np.int128).max:
                    col_dtype = 'int128'
                elif c_min >= np.iinfo(np.uint128).min and c_max <= np.iinfo(np.uint128).max:
                    col_dtype = 'uint128'

            elif dtype == 'float':
                # if c_min >= np.finfo(np.float16).min and c_max <= np.finfo(np.float16).max:
                #     col_dtype = 'float16'
                if c_min >= np.finfo(np.float32).min and c_max <= np.finfo(np.float32).max:
                    col_dtype = 'float32'
                elif c_min >= np.finfo(np.float64).min and c_max <= np.finfo(np.float64).max:
                    col_dtype = 'float64'

            elif dtype == 'object':
                if threshold > 0.7:
                    col_dtype = 'object'
                else:
                    col_dtype = 'category'
            col_dtypes[col] = col_dtype

        return col_dtypes

    def get_last_time(self, df):
        last_time = df.loc[df.shape[0]-1, 'candle_date_time_utc']
        last_time = ' '.join(last_time.split('T'))

        return last_time
        
    def get_market_code(self):
        market = self.machine.get_market_code()
        krw_market_code = [c for c in market['market'].to_list() if c.startswith('KRW')]

        return krw_market_code

    def set_columns_dtypes(self, df, type='daily'):
        assert type in ['daily', 'minutely'], "daily와 minuetely 중 하나를 택하세요."

        if type == 'daily':
            columns = {
                'market' : '시장-코인',
                'candle_date_time_utc' : '시각_utc',
                'candle_date_time_kst' : '시각_kst',
                'opening_price' : '시가',
                'high_price' : '고가',
                'low_price' : '저가',
                'trade_price' : '종가',
                'candle_acc_trade_price' : '누적거래금액',
                'candle_acc_trade_volume' : '누적거래량',
                'change_price' : '전일종가대비변화금액',
                'change_rate' : '전일종가대비변화량'
            }
            df = df.drop(columns=['timestamp', 'prev_closing_price']).rename(columns=columns)
            df = df.astype({'누적거래금액':np.int64, '누적거래량':np.int64})
            dtypes = self.check_dtypes(df)
            df = df.astype(dtypes)
            
        elif type == 'minutely':
            columns = {
                'market' : '시장-코인',
                'candle_date_time_utc' : '시각_utc',
                'candle_date_time_kst' : '시각_kst',
                'opening_price' : '시가',
                'high_price' : '고가',
                'low_price' : '저가',
                'trade_price' : '종가',
                'candle_acc_trade_price' : '누적거래금액',
                'candle_acc_trade_volume' : '누적거래량'
            }
            df = df.drop(columns=['timestamp', 'unit']).rename(columns=columns)
            df = df.astype({'누적거래금액':np.int64, '누적거래량':np.int64})
            dtypes = self.check_dtypes(df)
            df = df.astype(dtypes)

        return df

    def collect_minutely_all_data(self, markets:list):
        
        for market in markets:
            s = time.time()
            coin_df = pd.DataFrame()
            save_dir = DIR_UPBIT_MINUTELY_CANDLE + f'\\{market}.arr'
            latest_df = self.machine.get_minute_candle(unit=1, market=market, count=200)

            last_time = self.get_last_time(latest_df)
            coin_df = coin_df.append(latest_df, ignore_index=True)
            
            while True:
                df = self.machine.get_minute_candle(unit=1, market=market, to=last_time, count=200)
                if len(df.index) == 0:
                    break
                last_time = self.get_last_time(df)
                coin_df = coin_df.append(df, ignore_index=True)

            coin_df = self.set_columns_dtypes(coin_df, type='minutely')

            coin_df.to_feather(save_dir)
            print(f'{market} => Delta', time.time() - s)

    def collect_minutely_data_until_now(self, markets:list):

        for market in markets:
            s = time.time()
            load_dir = DIR_UPBIT_MINUTELY_CANDLE + f'\\{market}.arr'
            save_dir = DIR_UPBIT_MINUTELY_CANDLE + f'\\{market}.arr'

            old_df = pd.read_feather(load_dir)
            first_time = old_df.loc[0, 'candle_date_time_utc']

            latest_df = self.machine.get_minute_candle(unit=1, market=market, count=200)
            last_time = self.get_last_time(latest_df)

            first_time, last_time = parse(first_time), parse(last_time)
            
            if last_time <= first_time:
                subset_df = latest_df[latest_df['candle_date_time_utc'] > first_time]
                old_df = old_df.append(subset_df, ignore_index=True)
                old_df = self.set_columns_dtypes(old_df, type='minutely')

                old_df.to_feather(save_dir)
                print(f'{market} => Delta', time.time() - s)
                continue

            else:
                while True:
                    df = self.machine.get_minute_candle(unit=1, market=market, to=last_time)
                    last_time = self.get_last_time(df)
                    last_time = parse(last_time)

                    if last_time <= first_time:
                        subset_df = df[df['candle_date_time_utc'] > first_time]
                        old_df = old_df.append(subset_df, ignore_index=True)
                        old_df = self.set_columns_dtypes(old_df, type='minutely')
                        
                        old_df.to_feather(save_dir)
                        print(f'{market} => Delta', time.time() - s)
                        continue
                    old_df = old_df.append(df, ignore_index=True)

    def collect_daily_all_data(self, markets:list):
        
        for market in markets:
            s = time.time()
            coin_df = pd.DataFrame()
            save_dir = DIR_UPBIT_DAILY_CANDLE + f'\\{market}.arr'
            latest_df = self.machine.get_day_candle(market=market, count=200)

            last_time = self.get_last_time(latest_df)
            coin_df = coin_df.append(latest_df, ignore_index=True)
            
            while True:
                df = self.machine.get_day_candle(market=market, to=last_time, count=200)
                if len(df.index) == 0:
                    break
                last_time = self.get_last_time(df)
                coin_df = coin_df.append(df, ignore_index=True)

            coin_df = self.set_columns_dtypes(coin_df, type='daily')

            coin_df.to_feather(save_dir)
            print(f'{market} => Delta', time.time() - s)

    def collect_daily_data_until_now(self, markets:list):

        for market in markets:
            s = time.time()
            load_dir = DIR_UPBIT_DAILY_CANDLE + f'\\{market}.arr'
            save_dir = DIR_UPBIT_DAILY_CANDLE + f'\\{market}.arr'

            old_df = pd.read_feather(load_dir)
            first_time = old_df.loc[0, 'candle_date_time_utc']

            latest_df = self.machine.get_day_candle(market=market, count=200)
            last_time = self.get_last_time(latest_df)

            first_time, last_time = parse(first_time), parse(last_time)
            
            if last_time <= first_time:
                subset_df = latest_df[latest_df['candle_date_time_utc'] > first_time]
                old_df = old_df.append(subset_df, ignore_index=True)
                old_df = self.set_columns_dtypes(old_df, type='daily')

                old_df.to_feather(save_dir)
                print(f'{market} => Delta', time.time() - s)
                continue

            else:
                while True:
                    df = self.machine.get_day_candle(market=market, to=last_time)
                    last_time = self.get_last_time(df)
                    last_time = parse(last_time)

                    if last_time <= first_time:
                        subset_df = df[df['candle_date_time_utc'] > first_time]
                        old_df = old_df.append(subset_df, ignore_index=True)
                        old_df = self.set_columns_dtypes(old_df, type='daily')

                        old_df.to_feather(save_dir)
                        print(f'{market} => Delta', time.time() - s)
                        continue

                    old_df = old_df.append(df, ignore_index=True)                

