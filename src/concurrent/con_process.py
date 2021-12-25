"""
进程池是用来实现CPU密集任务
"""
from multiprocessing.context import Process
import time
import random
import os

# future 是一个python并发的公共接口，可以是线程也可以是进程
from concurrent import futures

import multiprocessing as mp


def expensive_function(n: int): 
    print(f"[PID = {os.getpid()}] (Parent process {os.getppid()}) Executing with {n = } ...")
    time.sleep(random.randint(1, 5))
    print(f"[PID = {os.getpid()}] {n = } Done.")
    

def execute_with_pool():
    tasks = [i for i in range(10)]
    print(f"启动进程池")
    with futures.ProcessPoolExecutor(max_workers=5) as pool:
        pool.map(expensive_function, tasks)


def execute_with_raw_process():
    worker = 10
    tasks = [i for i in range(worker)]
    process_pool = [mp.Process(target=expensive_function, 
                               args=(tasks[i], )) 
                    for i in range(worker)]
    
    for p in process_pool:
        p.start()
        
    for p in process_pool:
        p.join()

def put(q: mp.Queue): 
    stuff = ["an", object, 3]
    print(f"[PID: {os.getpid()}] Sleep 2 second")
    time.sleep(2)
    q.put(stuff)
    print(f"[PID: {os.getpid()}] Put {stuff = }")

def get(q: mp.Queue):
    print(f"[PID: {os.getpid()}] pulling {q}")
    a = q.get()
    print(f"[PID: {os.getpid()}] Get {a = }")
    
# 共享内存
def f1(n, a):
    n.value = 11111
    for i in range(len(a)):
        a[i] = -a[i]

def f2(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()


def share_with_primitives():
    num = mp.Value('d', 0.1)
    arr = mp.Array('i', range(10))

    p = Process(target=f1, args=(num, arr))
    p.start()
    p.join() # 主进程在这里阻塞
    
    print(num.value)
    print(arr[:])


def share_with_server_process():
    with mp.Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))

        p = Process(target=f2, args=(d, l))
        p.start()
        p.join()

        print(d)
        print(l)
    

def communicate_processes():
    
    q = mp.Queue()

    p1 = mp.Process(target=put, args=(q, ))
    p2 = mp.Process(target=get, args=(q, ))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()

    # 不是所有的东西都可以被Pickle的，不能被Pickle就不能用来通讯
    # p3 = mp.Process(target=lambda: print('?????'))
    # p3.start()
    # p3.join()

def f(l: mp.Lock, i):
    l.acquire() # 加锁，如果已经锁住，其他的进程会在这里阻塞
    try:
        print(f"[PID: {os.getpid()}] {i = } 得到锁，进行计算。。。")
    finally:
        l.release()
    

if __name__ == "__main__":
    
    # expensive_function(2)
    # execute_with_pool()
    # execute_with_raw_process()
    # communicate_processes()
    share_with_primitives()
    # share_with_server_process()
    
    #  进程同步
    # lock = mp.Lock()
    # ps = []
    # for num in range(10):
    #     p = mp.Process(target=f, args=(lock, num))
    #     ps.append(p)
    #     p.start()
        
    # for num in ps:
    #     num.join()