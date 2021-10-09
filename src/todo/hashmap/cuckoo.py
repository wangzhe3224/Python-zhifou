# Cuckoo Hashmap
from __future__ import annotations
from typing import Optional, Tuple, TypeVar, Union, List


KEY = TypeVar('KEY')
VAL = TypeVar('VAL')


def debug(msg):
    print(msg)


class Node:
    __solts__ = ['key', 'value']

    def __init__(self, key: KEY, value: VAL) -> None:
        self.key = key
        self.value = value
    
    def __repr__(self) -> str:
        return f"Node({self.key}: {self.value})"

# Optional[X] is equivalent to Union[X, None].
MAYBEVAL = Union[None, VAL] 
MAYBENODE = Union[None, Node] 

class HashTable:
    
    def __init__(self, size: int, retry: int=5) -> None:
        self._size = size
        self._num_records = 0
        self._ary1: List[MAYBENODE] = [None for _ in range(size//2)]
        self._ary2: List[MAYBENODE] = [None for _ in range(size//2)]
        self.__retry = retry
    
    def hash(self, s: KEY) -> Tuple[int, int]:
        # TODO: better hash
        x = hash(s)
        y = hash(hash(s))
        size = self._size // 2
        
        return x % size, y % size 

    def insert(self, k: KEY, d: VAL) -> bool:
        if self.find(k) is not None: 
            # TODO: overwrite Key - Value
            return False

        n = Node(k, d)

        if self._num_records >= (self._size // 2):
            self._grow_table()

        pos1, pos2 = self.hash(k)
        
        # probing
        pos: int = pos1
        table = self._ary1
        
        for _ in range(self.__retry):
            if table[pos] is None:
                table[pos] = n
                self._num_records += 1
                return True  # --> 
            
            # evict item in pos, n becomes vitim node
            # TODO: type not working here.. I know table[pos] here cannot be
            # None due to above branch, but mypy does not understand this..
            n, table[pos] = table[pos], n  # type: ignore

            if pos == pos1:
                pos1, pos2 = self.hash(n.key)
                pos = pos2
                table = self._ary2
            else:
                pos1, pos2 = self.hash(n.key)
                pos = pos1
                table = self._ary1
        
        # failed to find a good location, grow and reshape
        self._grow_table()
        self._reshape(self._size)
        return self.insert(n.key, n.value)
    
    def _grow_table(self) -> None:
        new_size = self._size * 2
        debug(f"grow table from {self._size} to {new_size}")
        self._reshape(new_size)
    
    def _reshape(self, new_size: int) -> None:
        # reset hash
        debug(f"reshaping table!")
        new_table = HashTable(new_size)
        for i in range(self._size // 2): 
            x, y = self._ary1[i], self._ary2[i]
            if x is not None:
                new_table.insert(x.key, x.value)
            if y is not None:
                new_table.insert(y.key, y.value)

        self._ary1 = new_table._ary1
        self._ary2 = new_table._ary2
        self._num_records = new_table._num_records
        self._size = new_table._size
        
    def find(self, k: KEY) -> MAYBEVAL:
        x, y = self._fetch(k)
        if x is not None and x.key == k: return x.value
        if y is not None and y.key == k: return y.value

        return None
    
    def delete(self, k: KEY) -> bool:
        pos1, pos2 = self.hash(k)
        x, y = self._ary1[pos1], self._ary2[pos2]
        if x is not None and x.key == k: 
            self._ary1[pos1] = None
        elif y is not None and y.key == k:
            self._ary2[pos2] = None
        else:
            return False 
        
        self._num_records -= 1
        return True
        
    def _fetch(self, k: KEY) -> Tuple[MAYBEVAL, MAYBEVAL]:
        pos1, pos2 = self.hash(k)
        x, y = self._ary1[pos1], self._ary2[pos2]
        return x, y

    def clone(self, left: HashTable, right: HashTable):
        ...

    def __str__(self) -> str:
        return f"{self._ary1} <> {self._ary2}"


def test():
    
    size = 55
    missing = 0
    found = 0 
    
    # create a hash table with an initially small number of bukets
    c = HashTable(100)
    
    # Now insert size key/data pairs, where the key is a string consisting
    # of the concatenation of "foobarbaz" and i, and the data is i
    inserted = 0
    for i in range(size): 
        if c.insert(str(i)+"foobarbaz", i):
            inserted += 1
    print("There were", inserted, "nodes successfully inserted")
        
    print(c)
        
    # Make sure that all key data pairs that we inserted can be found in the
    # hash table. This ensures that resizing the number of buckets didn't 
    # cause some key/data pairs to be lost.
    for i in range(size):
        ans = c.find(str(i)+"foobarbaz")
        if ans == None or ans != i:
            print(i, "Couldn't find key", str(i)+"foobarbaz")
            missing += 1
            
    print("There were", missing, "records missing from Cuckoo")
    
    # Makes sure that all key data pairs were successfully deleted 
    for i in range(size): 
        c.delete(str(i)+"foobarbaz")
        
    for i in range(size): 
        ans = c.find(str(i)+"foobarbaz") 
        if ans != None or ans == i: 
            print(i, "Couldn't delete key", str(i)+"foobarbaz") 
            found += 1
    print("There were", found, "records not deleted from Cuckoo") 


if __name__ == "__main__":
    
    test()