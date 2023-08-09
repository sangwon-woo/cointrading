import os
import pandas as pd

BASE = 'D:\\coin_database\\domestic\\upbit\\daily\\'

flist = os.listdir(BASE)

if __name__ == "__main__":
    for f in flist:
        df = pd.read_feather(BASE+f)
        print(df.head())
        break
