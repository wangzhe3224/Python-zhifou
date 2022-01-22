import threading
import weakref


class BigData:
    def __init__(self, key) -> None:
        ...
        

class Cache:
    
    def __init__(self) -> None:
        # self.pool = {}
        self.pool = weakref.WeakKeyDictionary()
        self.lock = threading.Lock()
        
    def get(self, key):
        
        with self.lock:
            data = self.pool.get(key)
            
            if data is not None:
                return data
            
            data = BigData(key)
            self.pool[key] = data
            
            return data