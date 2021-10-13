# 容器对象
import copy


a = [1,2,3]
aa = a
print(f"{id(a) = }")
print(f"{id(aa) = }")


b = [[1], [2], [3]]
c = copy.copy(b)
print(f"{b = }")
print(f"{c = }")
print(f"{id(b[0]) = }")
print(f"{id(c[0]) = }")
print(f"{id(b) = }")
print(f"{id(c) = }")

# b =[[1], [2], [3]]
# c =[[1], [2], [3]]

c[0] = ['???']
print(f"{b = }")
print(f"{c = }")
print(f"{id(b[0]) = }")
print(f"{id(c[0]) = }")


b = [[1], [2], [3]]
c = copy.deepcopy(b)
print(f"{b = }")
print(f"{c = }")
print(f"{id(b[0]) = }")
print(f"{id(c[0]) = }")
print(f"{id(b) = }")
print(f"{id(c) = }")


from __future__ import annotations


class A:
    
    def __init__(self) -> None:
        self.a = [1,2,3]
        self.b = {"1": 1}
    
    def __copy__(self) -> A:
        print(f"calling copy on {self}")
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        print(f"calling deepcopy on {self}")
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result


a = A()
b = copy.copy(a)
c = copy.deepcopy(a)
print(f"{id(a) = }")
print(f"{id(b) = }")
print(f"{id(c) = }")
print(f"{id(a.a) = }")
print(f"{id(b.a) = }")
print(f"{id(c.a) = }")