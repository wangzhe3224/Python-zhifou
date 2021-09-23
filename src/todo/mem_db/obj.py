import uuid
from memory_profiler import profile


class Data:
    def __init__(self) -> None:
        self.data = 1
        self.ttt = 2

class Target:
    
    def __init__(self) -> None:
        self.a = []
        self.b = {str(uuid.uuid4()): i for i in range(100_00)}
        self.c = (1,2,3,5)
        self.d = {"a": self.a}
        self.data = Data()

    def m1(self):
        return 12


if __name__ == '__main__':

    from mem_debugger import Debugger
    t = Target()
    db = Debugger(t, freq=2)
    db.start()
    
    import time
    time.sleep(5)
    # Destory target
    t = None