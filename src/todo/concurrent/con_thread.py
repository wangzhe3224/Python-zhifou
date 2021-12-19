""" 并发实现：线程

> CPython implementation detail: 
In CPython, due to the Global Interpreter Lock, only one thread can execute
 Python code at once (even though certain performance-oriented libraries might 
 overcome this limitation). If you want your application to make better use of 
 the computational resources of multi-core machines, you are advised to use 
 multiprocessing or concurrent.futures.ProcessPoolExecutor. 
 
 However, threading is still an appropriate model if you want to run multiple 
 I/O-bound tasks simultaneously.
"""
import threading
from threading import Thread, get_ident
from queue import Queue
import time
import random
import os 

from concurrent import futures


def expensive_function(n: int): 
    print(f"[PID = {os.getpid()}] (Parent process {os.getppid()}) \
          [TID = {get_ident()}] Executing with {n = } ...")
    time.sleep(random.randint(1, 5))
    print(f"[PID = {os.getpid()}] [TID = {get_ident()}] {n = } Done.")

def serial_execute():
    for i in range(5):
        expensive_function(i)

    
def execute_with_pool():
    tasks = [i for i in range(10)]
    print(f"启动线程池")
    with futures.ThreadPoolExecutor(max_workers=5) as pool:
        pool.map(expensive_function, tasks)


def execute_with_raw_threads():
    worker = 10
    tasks = [i for i in range(worker)]
    thread_pool = [Thread(target=expensive_function, args=(tasks[i], )) 
                   for i in range(worker)]
    
    for p in thread_pool:
        p.start()
        
    for p in thread_pool:
        p.join()


def thread_worker_func(q: Queue, other_args):
    arg = q.get()  # <-- 阻塞
    expensive_function(arg)  # 任务函数


def communication_thread():
    q = Queue()
    threads = []
    for i in range(10):
        q.put(i)
        t = Thread(target=thread_worker_func, args=(q, i))
        threads.append(t)
        print(f"启动线程 for {i}")
        t.start()
        
    for t in threads:
        t.join()
    

# 共享内存
def add_and_read_key(d, key):
    # 但是，这里有race condition，共享内存虽然更容易，但是race问题不能避免
    print(f"add key {key}")
    d[key] = key
    print(f"dict is {d}") # 这里打印的结果不是完全确定的，根据系统调度线程的情况。


def share_is_easier_in_thread():
    a = {}
    
    t1 = Thread(target=add_and_read_key, args=(a, 't1'))
    t2 = Thread(target=add_and_read_key, args=(a, 't2'))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
        

# 同步
# 1. Lock
"""
When more than one thread is blocked in acquire() waiting for the state to turn
to unlocked, only one thread proceeds when a release() call resets the state to unlocked
"""
lock = threading.Lock()

def lock_add_and_read(d, key):
    with lock:
        add_and_read_key(d, key)

def access_resource_with_lock():
    a = {}
    
    t1 = Thread(target=add_and_read_key, args=(a, 't1'))
    t2 = Thread(target=add_and_read_key, args=(a, 't2'))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

# 其他同步原语：Condition, Event, Barrier, Timer
"""
cv = threading.Condition()

# Consume one item
with cv:
    while not an_item_is_available():
        cv.wait()
    get_an_available_item()

# Produce one item
with cv:
    make_an_item_available()
    cv.notify()
"""     

if __name__ == '__main__':
    
    # serial_execute()
    # execute_with_pool()
    # execute_with_raw_threads()
    # share_is_easier_in_thread()
    communication_thread()
    # access_resource_with_lock()