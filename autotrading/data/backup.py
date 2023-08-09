import shutil
import os
from config.setting import *
import time
from util.util import time_print


def backup_start(source, destination, file_ext):
    s = time.time()
    data_files = [f for f in os.listdir(source) if f.endswith(file_ext)]
    count_files = len(data_files)
    print(f'Total File Counts: {count_files}')

    for idx, data_file_name in enumerate(data_files):
        load_path = source + f'\\{data_file_name}'

        if not os.path.isdir(destination):
            os.makedirs(destination)
            print(f'Made dirs => {destination}')

        save_path = destination + f'\\{data_file_name}'

        if not os.path.exists(save_path):
            shutil.copy(load_path, save_path)
            print(f'Copy {data_file_name} complete({idx+1}/{count_files})')
        else:
            os.remove(save_path)
            shutil.copy(load_path, save_path)
            print(f'Copy {data_file_name} complete({idx+1}/{count_files})')

    print(f'Backup Complete', end=' ')
    time_print(s, time.time())
