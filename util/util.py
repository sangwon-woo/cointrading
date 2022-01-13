import pandas as pd
import datetime


def time_print(start_time, end_time):
    delta = end_time - start_time
    hours = delta // 3600
    minutes = (delta - (hours * 3600)) // 60
    seconds = (delta - (hours * 3600) - (minutes * 60)) % 60
    if hours:
        if minutes:
            print(f'{hours}시간 {minutes}분 {seconds:.2f}초')
        else:
            print(f'{hours}시간 {seconds:.2f}초')
    else:
        if minutes:
            print(f'{minutes}분 {seconds:.2f}초')
        else:
            print(f'{seconds:.2f}초')


def get_first(s):
    return s.iloc[-1]


def get_last(s):
    return s.iloc[0]


def aggregate_candle_with_timeframe(original_df, start_date=None, end_date=None, timeframe=1, unit='day') -> pd.DataFrame:
    original_df['날짜'] = pd.to_datetime(original_df['시각_utc']).dt.date
    original_df['시간'] = pd.to_datetime(original_df['시각_utc']).dt.time

    start_date = start_date if start_date else original_df['시각_utc'].min()
    end_date = end_date if end_date else original_df['시각_utc'].max()

    original_df = original_df[
        (original_df['시각_utc'] >= start_date) &
        (original_df['시각_utc'] <= end_date)
    ]

    agg_func = {
        '시가': get_first,
        '고가': 'max',
        '저가': 'min',
        '종가': get_last,
        '누적거래금액': 'sum',
        '누적거래량': 'sum'
    }

    if unit == 'day':
        if timeframe == 1:
            grouped = original_df.groupby('날짜')
            ret = grouped[['시가', '고가', '저가', '종가', '누적거래금액', '누적거래량']].agg(
                agg_func).reset_index().sort_values('날짜', ascending=False).reset_index(drop=True)
        else:
            basis = timeframe
    elif unit == 'minute':
        denominator = timeframe
        pass

    return ret
