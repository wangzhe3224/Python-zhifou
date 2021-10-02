from __future__ import annotations
from abc import ABC, abstractmethod

class Command(ABC):
    
    @abstractmethod
    def execute(self):
        ...
        
class SimpleCommand(Command):
    
    def __init__(self, payload: str) -> None:
        self._payload = payload
        
    def execute(self):
        print(f"SimpleCommand execute with {self._payload}")

class ComplexCommand(Command):
    
    def __init__(self, receiver: Receiver, a, b) -> None:
        self._a = a
        self._b = b
        self._receiver = receiver
    
    def execute(self):
        print(f"ComplexCommand execute with {self._receiver}")
        self._receiver.do_a(self._a)
        self._receiver.do_b(self._b)


class Receiver:
    """ 包含了业务逻辑，即知道如何响应命令。 """

    def do_a(self, a: str):
        print(f"{self} do a with {a}")
        
    def do_b(self, b: str):
        print(f"{self} do b with {b}")


class Invoker:
    """  """
    def set_on_start(self, command: Command):
        self._on_start = command

    def set_on_finish(self, command: Command):
        self._on_finish = command

    def do_something_important(self) -> None:
        if isinstance(self._on_start, Command):
            self._on_start.execute()
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()

if __name__ == '__main__':
    invoker = Invoker()
    invoker.set_on_start(SimpleCommand("Say Hi!"))
    receiver = Receiver()
    invoker.set_on_finish(ComplexCommand(
        receiver, "Send email", "Save report"))
    invoker.do_something_important() 