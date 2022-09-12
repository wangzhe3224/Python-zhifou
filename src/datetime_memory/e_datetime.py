import sys
import pandas as pd
import numpy as np
from datetime import datetime


from collections.abc import Mapping, Container
from sys import getsizeof
 
def deep_getsizeof(o, ids=set()):
    """Find the memory footprint of a Python object
 
    This is a recursive function that drills down a Python object graph
    like a dictionary holding nested dictionaries with lists of lists
    and tuples and sets.
 
    The sys.getsizeof function does a shallow size of only. It counts each
    object inside a container as pointer only regardless of how big it
    really is.
 
    :param o: the object
    :param ids:
    :return:
    """
    d = deep_getsizeof
    if id(o) in ids:
        return 0
 
    r = getsizeof(o)
    ids.add(id(o))
 
    if isinstance(o, str) or isinstance(0, str):
        return r
 
    if isinstance(o, Mapping):
        return r + sum(d(k, ids) + d(v, ids) for k, v in o.iteritems())
 
    if isinstance(o, Container):
        return r + sum(d(x, ids) for x in o)
 
    return r 

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


d1 = datetime(2022, 1, 2, 12, 30, 11, 123)
pd1 = pd.Timestamp(d1)
nd1 = np.datetime64(d1)

print(f"size of d1 = {deep_getsizeof(d1, set())} bytes")
print(f"size of pd1 = {deep_getsizeof(pd1, set())} bytes")
print(f"size of nd1 = {deep_getsizeof(nd1, set())} bytes")
# size of d1 = 48 bytes
# size of pd1 = 112 bytes
# size of nd1 = 40 bytes


# Index
index = pd.date_range('2022-01-01', '2022-08-01', freq='1s')
np_index = np.arange('2022-01-01', '2022-08-01', dtype='datetime64[s]')
idx = np.random.choice(range(len(index)), len(index)//2, replace=False)
random_picked = index[idx]

s1 = pd.Series(data=np.random.rand(len(index)), index=index)

random_ts = []
for i in random_picked:
    random_ts.append(i)
    
