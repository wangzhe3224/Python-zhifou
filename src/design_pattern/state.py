from __future__ import annotations
from abc import ABC, abstractmethod


class Context:
    """ Context 是包含 State 的对象，也就是 state 的客户端 """
    
    _state = None
    
    def __init__(self, state: State) -> None:
        self.transition_to(state)
    
    def transition_to(self, state: State):
        self._state = state
        self._state.context = self
    
    def request1(self):
        self._state.handle1()

    def request2(self):
        self._state.handle2()


class State(ABC):
    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def handle1(self):
        ...
        
    @abstractmethod
    def handle2(self):
        ...


# 我们的状态机有两个状态，A 和 B
class ConcreteStateA(State):
    def handle1(self) -> None:
        print("ConcreteStateA handles request1.")
        print("ConcreteStateA wants to change the state of the context.")
        self.context.transition_to(ConcreteStateB())

    def handle2(self) -> None:
        print("ConcreteStateA handles request2.")    

class ConcreteStateB(State):
    def handle1(self) -> None:
        print("ConcreteStateB handles request1.")

    def handle2(self) -> None:
        print("ConcreteStateB handles request2.")
        print("ConcreteStateB wants to change the state of the context.")
        self.context.transition_to(ConcreteStateA())


if __name__ == "__main__":
    context = Context(ConcreteStateA())
    context.request1()
    context.request2()