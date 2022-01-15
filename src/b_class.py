
class MyClass:
    """ 
    I am a doc str
    """

    c = 1
    
    def __init__(self) -> None:
        self.a = 1
        self.b = 2

    @classmethod
    def aa(cls):
        ...

    @staticmethod
    def ss():
        ...

my = MyClass()























# Weak ref
import weakref
wref = weakref.ref(my)
my2 = wref()
del my, my2