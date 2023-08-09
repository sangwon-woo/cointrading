import multiprocessing as mp
import random
import time
from util.util import time_print


def get_partial_list(code_list, cpu_count):
    code_cnt = len(code_list)
    idx = code_cnt // cpu_count
    random.shuffle(code_list)

    start = 0
    end = idx + 1
    for i in range(cpu_count):
        tmp_list = code_list[start:end]
        yield tmp_list

        start = end
        end += (idx + 1)

        if end > code_cnt:
            end = code_cnt


def collect_data_with_multiprocess(type, collector, market_code_i_have, cpu_count):
    assert type in ['daily', 'minutely'], 'Wrong Type!'

    s = time.time()

    processes = []

    print(f'{type} 데이터 업데이트 시작')

    if type == 'daily':
        for code in get_partial_list(market_code_i_have, cpu_count):
            proc = mp.Process(
                target=collector.collect_daily_data_until_now, args=(code,)
            )
            processes.append(proc)
    elif type == 'minutely':
        for code in get_partial_list(market_code_i_have, cpu_count):
            proc = mp.Process(
                target=collector.collect_minutely_data_until_now, args=(code,)
            )
            processes.append(proc)
    for p in processes:
        p.start()

    for p in processes:
        p.join()

    e = time.time()
