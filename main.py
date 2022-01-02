import multiprocessing as mp
from autotrading.strategy import Strategy
from autotrading.trading import Trading
from autotrading.data.collector import Collector

# 어차피 나중에는 모두 백그라운드 프로세스(daemon=True)가 될 수밖에 없음.
# 웹앱으로 만들어서 실시간 데이터 수신, 매매전략 실행, 매매 성과평가 등을 보여주자.

if __name__ == '__main__':
    while True:
        break
    # 데이터를 실시간으로 받기

    # 실시간 데이터를 db와 arr 파일로 저장하기

    # 각 매매 전략의 매매 신호를 확인하기

    # 매매 신호가 발생한 매매 전략 실행하기
