from threading import Thread
import time
import random
import os 

from concurrent import futures


def expensive_function(n: int): 
    print(f"[PID = {os.getpid()}] (Parent process {os.getppid()}) Executing with {n = } ...")
    time.sleep(random.randint(1, 5))
    print(f"[PID = {os.getpid()}] {n = } Done.")

def serial_execute():
    for i in range(10):
        expensive_function(i)

    
def execute_with_pool():
    tasks = [i for i in range(10)]
    print(f"启动线程池")
    with futures.ThreadPoolExecutor(max_workers=5) as pool:
        pool.map(expensive_function, tasks)


def execute_with_raw_threads():
    worker = 10
    tasks = [i for i in range(worker)]
    thread_pool = [Thread(target=expensive_function, args=(tasks[i], )) for i in range(worker)]
    
    for p in thread_pool:
        p.start()
        
    for p in thread_pool:
        p.join()


def add_and_read_key(d, key):
    # 但是，这里有race condition，共享内存虽然更容易，但是race问题不能避免
    print(f"add key {key}")
    d[key] = key
    print(f"dict is {d}") # 这里打印的结果不是完全确定的，根据系统调度线程的情况。

# 共享内存
def share_is_easier_in_thread():
    a = {}
    
    t1 = Thread(target=add_and_read_key, args=(a, 't1'))
    t2 = Thread(target=add_and_read_key, args=(a, 't2'))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
        
        
if __name__ == '__main__':
    
    # serial_execute()
    # execute_with_pool()
    # execute_with_raw_threads()
    share_is_easier_in_thread()