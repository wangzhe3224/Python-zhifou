from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class Subject(ABC):
    """ The Subject interface declares a set of methods for managing subscribers.  """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """ Attach an observer to the subject.  """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """ Detach an observer from the subject.  """
        pass

    @abstractmethod
    def notify(self) -> None:
        """ Notify all observers about an event.  """
        pass


class ConcreteSubject(Subject):
    """ The Subject owns some important state and notifies observers when the state
    changes.
    """

    _state: int = None
    """ For the sake of simplicity, the Subject's state, essential to all
    subscribers, is stored in this variable.
    """

    _observers: List[Observer] = []
    """ List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        """ Trigger an update in each subscriber.  """
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self) -> None:
        print("\nSubject: I'm doing something important.")
        self._state = randrange(0, 10)
        print(f"Subject: My state has just changed to: {self._state}")
        self.notify()


class Observer(ABC):
    """ The Observer interface declares the update method, used by subjects.  """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """ Receive update from subject.  """
        pass


class ConcreteObserverA(Observer):
    def update(self, subject: Subject) -> None:
        if subject._state < 3:
            print("ConcreteObserverA: Reacted to the event")


class ConcreteObserverB(Observer):
    def update(self, subject: Subject) -> None:
        if subject._state == 0 or subject._state >= 2:
            print("ConcreteObserverB: Reacted to the event")


if __name__ == "__main__":
    # The client code.

    subject = ConcreteSubject()

    observer_a = ConcreteObserverA()
    subject.attach(observer_a)

    observer_b = ConcreteObserverB()
    subject.attach(observer_b)

    subject.some_business_logic()
    subject.some_business_logic()

    subject.detach(observer_a)

    subject.some_business_logic()