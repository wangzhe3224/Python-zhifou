from typing import List
import threading
import collections
import asyncio
import tracemalloc
import weakref
import logging
import traceback
import linecache
import os
import sys

import guppy
from guppy import hpy
# from pympler import asizeof # this import takes 6 MB memory....
logging.basicConfig(level = logging.INFO)

heap = hpy()
MB = 1024 * 1024
logger = logging.getLogger('MemDebugger')
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


def filter_stats(stats: List[tracemalloc.Statistic], key: str):
    return [i for i in stats if key in str(i)]
        

def extract_stats(snapshot: tracemalloc.Snapshot):
    stat = snapshot.statistics('traceback')
    stat = filter_stats(stat, 'obj')
    for item in stat:
        logger.info(item)
    # for l in stat.traceback.format():
    #     print(l)


def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print("#%s: %s:%s: %.1f KiB"
              % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


class Debugger:

    def __init__(self, target: object, freq: int=60, max_snapshots: int=30) -> None:
        print(f"Creating weakref of {target} @ {id(target)}")
        print(f"Debugger address {id(self)}")
        self.target: weakref.ref = weakref.ref(target, self.callback)

        self.freq = freq
        self.max_snapshots = max_snapshots

        self.snapshots = collections.deque(maxlen=self.max_snapshots)

        self.__loop = None
        self.__thread = threading.Thread(target=self._start)
        self.__running = True

        tracemalloc.start()

    def callback(self, ref):
        # when the target object losing strong reference
        print(f"Target {ref} is dead, stop debug {self}")
        self.__running = False
        self.__loop.stop()

    async def check_loop(self):

        while self.__running:
            # Checking logic
            sp = tracemalloc.take_snapshot()
            try:
                print(f"{sp}")
                extract_stats(sp)
                # display_top(sp)
                self.snapshots.append(sp)
            except Exception as e:
                logger.warning(f"Failed to extract snapshop")
                logger.warning(traceback.format_exc())

            await asyncio.sleep(self.freq)

    def _start(self):
        # Get its own event loop
        policy = asyncio.get_event_loop_policy()
        policy.set_event_loop(policy.new_event_loop())
        self.__loop = asyncio.get_event_loop()
        # self.__loop.create_task(self.check())
        try:
            self.__loop.run_until_complete(self.check_loop())
        except RuntimeError:
            print(f"Exit.")
    
    def start(self):
        self.__thread.start()
