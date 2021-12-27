import shutil
import os
from config.setting import *
import time

def backup_start(source, destination, file_ext):
    s = time.time()
    data_files = [f for f in os.listdir(source) if f.endswith(file_ext)]
    count_files = len(data_files)
    print(f'Total File Counts: {count_files}')

    for data_file_name in data_files:
        load_path = source + f'\\{data_file_name}'

        # if not os.path.isdir(destination):
        #     os.makedirs(destination)
        #     print(f'Made dirs => {destination}')

        save_path = destination + f'\\{data_file_name}'
        print(load_path, save_path)
        # if not os.path.exists(save_path):
        #     shutil.copy(load_path, save_path)
        #     print(f'Copy {data_file_name} complete')
        # else:
        #     os.remove(load_path)
        #     shutil.copy(load_path, save_path)

    print(f'Backup Complete(Spent time : {(time.time() - s):.2f}초)')


if __name__ == '__main__':
    backup_start(DIR_UPBIT_DAILY_CANDLE, DIR_UPBIT_DAILY_CANDLE_BACKUP, '.arr')
    backup_start(DIR_UPBIT_MINUTELY_CANDLE, DIR_UPBIT_MINUTELY_CANDLE_BACKUP, '.arr')