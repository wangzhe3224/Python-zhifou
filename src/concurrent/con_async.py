"""
async / await

> asyncio is often a perfect fit for IO-bound and high-level
> structured network code.

高级开发技巧: https://docs.python.org/3/library/asyncio-dev.html
"""
from asyncio.tasks import sleep
import os, time, random
from threading import get_ident
import time

import asyncio

# basics
# coroutine
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def expensive_function(n: int): 
    print(f"[PID = {os.getpid()}] (Parent process {os.getppid()}) \
          [TID = {get_ident()}] Executing with {n = } ...")
    # time.sleep(random.randint(1, 5))
    await asyncio.sleep(random.randint(1, 5))
    print(f"[PID = {os.getpid()}] [TID = {get_ident()}] {n = } Done.")


async def run_in_async():
    tasks = []   
    for i in range(10):
        tasks.append(asyncio.create_task(expensive_function(i)))

    res = await asyncio.gather(*tasks)

## 同步
# Lock, Event, Condition, Semaphore
# 虽然 async 是单线程并发，锁还是有用的，比如可以确保某个代码只会被执行一次
key = False

async def request_by_many():
    lock = asyncio.Lock()
    async with lock:
        if key is False:
            await only_run_once()

async def only_run_once():
    global key
    print(f"Only run once function called")
    key = True
    await asyncio.sleep(1)

        
async def with_lock():
    tasks = []
    for i in range(10):
        tasks.append(asyncio.create_task(request_by_many()))
    
    await asyncio.gather(*tasks)

# Event
async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')

async def with_wait():
    # Create an Event object.
    event = asyncio.Event()

    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.create_task(waiter(event))

    # Sleep for 1 second and set the event.
    await asyncio.sleep(1)
    # time.sleep(1) # <<< 
    event.set()

    # Wait until the waiter task is finished.
    await waiter_task

    
# 通讯：Queue
# 注意，async的queue没有timeout，如果需要timeout，需要使用 asyncio.wait_for()
async def worker(name, queue):
    while True:
        sleep_for = await queue.get()
        
        await asyncio.sleep(sleep_for)
        
        queue.task_done()  # 通知队列任务完成了, blocking loop
        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def with_queue():
    
    q = asyncio.Queue()
    
    total = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1)
        total += sleep_for
        q.put_nowait(sleep_for)
        
    # 创建worker
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f"worker-{i}", q))
        tasks.append(task)

    start_at = time.monotonic()
    await q.join()
    total_slept = time.monotonic() - start_at   
    
    # 摧毁worker
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    print('====')
    print(f'3 workers slept in parallel for {total_slept:.2f} seconds')
    print(f'total expected sleep time: {total:.2f} seconds')
    

if __name__ == '__main__':
    
    # Coroutines
    async def main():
        print(f"started at {time.strftime('%X')}")

        await say_after(1, 'hello')
        await say_after(2, 'world')

        print(f"finished at {time.strftime('%X')}")
    
    # Task: schedule coroutines concurrently.
    async def main2():
        t1 = asyncio.create_task(say_after(1, 'hello'))
        t2 = asyncio.create_task(say_after(2, 'world'))
        print(f"started at {time.strftime('%X')}")

        await t1
        await t2

        print(f"finished at {time.strftime('%X')}")

    # Future: Future object is awaited it means that the coroutine will 
    # wait until the Future is resolved in some other place
    # Normally there is no need to create Future objects at the application level code.
    # Future objects in asyncio are needed to allow callback-based code to be used with async/await.

    # print(main())   # Sync
    # asyncio.run(main())
    # asyncio.run(main2())  # Async
    # asyncio.run(run_in_async())
    # asyncio.run(with_lock())
    # asyncio.run(with_wait())
    asyncio.run(with_queue())