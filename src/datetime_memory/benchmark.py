import inspect
import pandas as pd
import numpy as np
import polars as pl
from datetime import datetime
import random
from memray import Tracker
import pytz

from datetime import date


HK_TZ = pytz.timezone("Asia/Hong_Kong")

def generate_polars_index():
    
    func = inspect.stack()[0][3]
    with Tracker(f"{func}.bin", native_traces=True):
        index = pl.date_range(date(2022, 1, 1), date(2022, 8, 1), "1s", name="drange", time_unit='ms')

    return index


def generate_a_lot_datetime(n: int = 1_000_000, tz: bool=False):
    
    with Tracker("generate_a_lot_datetime.bin", native_traces=True):
        res = []   
        for i in range(n):
            if tz:
                res.append(datetime(2022, random.randint(1, 12), random.randint(1, 28), 1, 1, 1, i%1000, tzinfo=HK_TZ))
            else:
                res.append(datetime(2022, random.randint(1, 12), random.randint(1, 28), 1, 1, 1, i%1000))

    return res

def generate_a_lot_datetime64(n: int = 1_000_000):

    with Tracker("generate_a_lot_datetime64.bin", native_traces=True):
        res = []   
        for i in range(n):
            res.append(np.datetime64(f"2022-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}T01:02:03.123"))

    return res
    

def generate_a_lot_Timestamp(n: int = 1_000_000):

    with Tracker("generate_a_lot_Timestamp.bin", native_traces=True):
        res = []   
        for i in range(n):
            res.append(pd.Timestamp(f"2022-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}T01:02:03.123"))

    return res

    
def generate_large_pd_index():

    func = inspect.stack()[0][3]
    with Tracker(f"{func}.bin", native_traces=True):
        index = pd.date_range('2022-01-01', '2022-08-01', freq='1s')

    print(f"Length of index: {len(index)}")
    return index


def generate_large_np_index():

    func = inspect.stack()[0][3]
    with Tracker(f"{func}.bin", native_traces=True):
        index = np.arange('2022-01-01', '2022-08-01', dtype='datetime64[s]')

    print(f"Length of index: {len(index)}")
    return index

if __name__ == "__main__":
    
    # res = generate_a_lot_datetime(tz=True)
    # res = generate_a_lot_datetime(tz=False)

    # res = generate_a_lot_datetime64()

    # res = generate_a_lot_Timestamp()

    # generate_large_pd_index()

    # generate_large_np_index()

    generate_polars_index()

    # [x] todo: use memray's API to measure memory usage of: datetime, datetime64, Timestamp?
    # [x] todo: which one to use?
    # [x] todo: what about timezone info?
    # todo: pyarrow datetime?
    # todo: how can we reduce timestamp index/column in dataframe for high frequence data?
    # doc reference : https://hackmd.io/sxxQnM5jTxK7D-7ZN5ok3Q