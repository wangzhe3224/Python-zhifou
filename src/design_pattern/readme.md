# 重拾面向对象设计模式

> Python的视角
> 转载请注明出处。
> 代码见：https://github.com/wangzhe3224/Python-zhifou/tree/master/src/todo/design_pattern

- [重拾面向对象设计模式](#重拾面向对象设计模式)
  - [引言](#引言)
  - [创造模式，Creational Patterns](#创造模式creational-patterns)
    - [工厂方法，Factory Method](#工厂方法factory-method)
    - [抽象工厂，Abstract Factory](#抽象工厂abstract-factory)
    - [建造者，Builder](#建造者builder)
    - [单例，Singleton](#单例singleton)
    - [原型，Prototype](#原型prototype)
    - [总结](#总结)
  - [结构模式，Structural Patterns](#结构模式structural-patterns)
    - [组合，Composite](#组合composite)
    - [转换器、桥接、装饰器、代理](#转换器桥接装饰器代理)
    - [总结](#总结-1)
  - [行为模式，Behavior Patterns](#行为模式behavior-patterns)
    - [访问者，Visitor](#访问者visitor)
    - [观察者，Observer](#观察者observer)
    - [命令，Command](#命令command)
    - [迭代器，Iterator](#迭代器iterator)
    - [备忘录，Memento](#备忘录memento)
    - [策略，Strategy](#策略strategy)
    - [状态机，State](#状态机state)
  - [总结](#总结-2)
  - [参考](#参考)

## 引言

面向对象设计模式就是一系列的组织类和对象的方法，这些方法的目的就是产生更加清晰，且容易拓展和
修改的代码。但是，如果我们翻开设计模式的教科书，我们会发现很多的名词，但是这其中很多的模式仅仅
是由于语言的限制所产生的的。因为有些语言缺乏函数一等公民或者属于静态类型等等。

尽管如此，学习设计模式仍然非常有用，只不过我们可能需要换一种角度重新审视这些设计模式，去思考
这些模式背后的原则：

- 面对接口编程，而不是面对实现
- 延迟执行，即不到不得不实例化的时候，选择延迟

这两个原则不光在面向对象编程中成立，他们在任何一种语言范式中都存在。这两个原则的核心在于如何管理
依赖，而管理依赖的方法就是隐藏（或者说封装）和依赖注入。这篇文章我们就讨论如何将这些原则应用到
传统的设计模式中：

- 创造模式，Creational Patterns
- 结构模式，Structural Patterns
- 行为模式，Behavioral Patterns

## 创造模式，Creational Patterns

创造模式主要是提供一些实例化对象的模式，主要包括：

- 工厂方法
- 抽象工厂
- 建造者
- 原型
- 单例

这些创造模式都是关于实例化一个或者若干个相关的对象的，让我们来看看他们是怎么用到上述两个原则的。
下面的小节有如下结构：面临的问题、解决方案、跟原则的关系。由于我们是用Python举例的，Python的
很多语言特性，比如鸭子类型、函数一等公民等等，可能会让这些模式看起来与传统的设计模式不太一样，
但是，道理是一样的。当然，如果考虑一些更加强大类型系统，比如代数数据类型，很多问题甚至都不存在，
比如抽象工厂想要解决的问题，实际上就是 Sum Type 和 Product Type 的组合。。

### 工厂方法，Factory Method

假设我们有如下类，`RobotController` 包含一个 `Robot` 对象，然后可以控制它，
比如 `some_function`。

```python
class Robot:
    
    def move(self):
        print(f"{self} moves.")

class RobotController:

    def __init__(self):
        self.robot = Robot()  # <-- 注意这里，Controller提前实例化的其他的对象，就产生了依赖。

    def some_function(self):
        print(f"Play with {self.robot}")
        self.robot.move()
```

看起来不错，现在问题来了，这个Controller现在需要为控制另一种机器人，`RobotB`

``` python
class RobotB:

    def move(self):
        print(f"{self} moves.")
```

这时，我们的 controller 类就需要更改代码，才能支持新的 RobotB。其实问题的关键在于
 controller 过早的实例化 Robot 导致了依赖。这时候我们可以给controller注入一个工厂类，
 这个类负责对象的实例化，从而把责任委托给工厂类。而这个工厂类应该是一个抽象（接口）才能保证
 controller 代码可以实用与更多的不同类型的 Robot。

```python
from abc import abstractmethod

class RobotInterface:

    @abstractmethod
    def move():
        ...


class Robot(RobotInterface):
    
    def move(self):
        print(f"{self} moves.")

class RobotB(RobotInterface):
    
    def move(self):
        print(f"{self} moves.")

class RobotCreator:
    
    # >>>>>>>>   这个就是所谓的 工厂方法！   <<<<<>>>>>
    @abstractmethod
    def create() -> RobotInterface:
        ...


class RobotACreator(RobotCreator):

    def create(self) -> RobotInterface:
        return Robot()


class RobotBCreator(RobotCreator):

    def create(self) -> RobotInterface:
        return RobotB()


class RobotController:

    def __init__(self, creator: RobotCreator):
        # 原则1：针对抽象编程
        # 原则2：延后对象实例化
        # 原则3：委托责任（给 creator 对象）
        self.robot: RobotInterface = creator.create()

    def some_function(self):
        print(f"Play with {self.robot}")
        self.robot.move()

def main():
    creator_a = CreatorA()
    creator_b = CreatorB()
    controller = RobotController(creator_a)
    controller.move()
```

不过，对于Python来说，我们并不需要 `Creator` 这一层抽象，因为 Python 可以直接传递类。
我们可以直接：

``` python
# 省略 Creator 的版本
class RobotController:

    def __init__(self, robot_cls: RobotInterface):
        # 原则1：针对抽象编程
        # 原则2：延后对象实例化
        self.robot: RobotInterface = robot_cls() # 注意这里传递的 class 不是对象
        # 对于 Java 这种类不是一等公民的语言，Creator往往是必须的，因为只能传递对象。
        # 如果使用依赖注入，我们·可以直接传入一个对象，就省略了 （）

    def some_function(self):
        print(f"Play with {self.robot}")
        self.robot.move()
```

如果我们使用依赖注入，我们可以直接传入Robot对象，而不是类。

当然，并不是说 `Creator` 这一层抽象是没有意义的，当我们的对象实例化变得比价复杂的时候，即
不是一个 `class()` 可以搞定的时候，Creator 的工厂方法 `create` 可以做很多复杂的工作。
我举个简单的例子，比如我们希望实例化 RobotB 的时候打印一些信息，我们就可以把相应的逻辑放入
`create` 内部，而不需要让其他的类负责。

我再举个例子，如果Robot的构造变得更加复杂了，比如需要组装不同的部件才能获得一个实例，Creator
这层抽象就显得是必须的。当然，这里不讨论依赖注入，即使使用依赖注入，直接传递实例化以后的对象，
实例化这个对象的复杂度仍然需要一个对象来负责。这里就引出了下一个创造模式：抽象工厂。

### 抽象工厂，Abstract Factory

我们延续上一个例子，现在机器人变得复杂了，我们需要两个部件组装一个机器人：外壳和灵魂。而每种
部件还可能存在不同的类型，比如金属、塑料、液体等等，电子灵魂、人类灵魂等等。这时候为了生产
不同的外壳和灵魂组合，我们需要抽象工厂。再一次，对于Python这不是最优雅的实现。

``` python
class RobotI:
    
    @abstractmethod
    def move(self):
        ...

class Robot(RobotI):

    def __init__(self, shell, soul):
        self.shell = shell
        self.soul = soul
    
    def move(self):
        print(f"Robot with {self.shell} and {self.soul} moves")

class FactoryI:

    @abstractmethod
    def create_shell(self):
        ...

    @abstractmethod
    def create_soul(self):
        ...

    def create(self):
        shell = self.create_shell()
        soul = self.create_soul()
        return Robot(shell, soul)

class MetalDigitalRobotFactory(FactoryI):
    
    def create_shell(self):
        return MetalShell() 

    def create_soul(self):
        return DigitalSoul()


class App:

    def __init__(self, factory: FactoryI):
        # 注意这里依赖被转移到了factory
        # App 中的逻辑代码不再依赖于 Robot 的具体组装和实现
        self.robot: RobotI = factory.create()

def main():
    factory = MetalDigitalRobotFactory()
    app = App(factory)
```

这里，我们可以通过增加新的工厂轻松的拓展我们的代码，而不用触碰已有的代码。下游的控制类并不需要
知道制造机器人的复杂度，因为他们不负责实例化机器人，也不必知道机器人的类型，因为他们是针对接口
编程的。

不过，在Python这类动态语言中，我们可以简化工厂类成几个函数：

```python
def create_metal_digital_robot() -> RobotI:
    shell = MetalShell() 
    soul = DigitalSoul()
    return Robot(shell, soul)

class App:

    def __init__(self, factory: callable):
        self.robot: RobotI = factory()

def main():
    factory = MetalDigitalRobotFactory()
    app = App(factory = create_metal_digital_robot)
```

### 建造者，Builder

建造者模式其实与抽象工厂异曲同工，都是把一个复杂的对象实例化过程封装在一个对象里，而这个builder
抽象通过他不同的实现，生产不同的对象。

### 单例，Singleton

单例其实就是一个特殊的工厂，他的`create`方法永远返回唯一的一个对象，这里是指在同一个内存地址的
同一个对象。只不过，按照惯例，Singleton的创造方法一般被叫做`get_instance`。

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # 如果不存在，就创建一个对象
            cls._instance = super(Singleton, cls).__new__(cls)
        # 永远返回同一对象。
        return cls._instance
```

### 原型，Prototype

原型试图解决的是另一个问题：如果复制一个对象。之前的讨论的模式都是如何初始化（实例化）一个对象。
即实现一个 `clone` 方法。这样做的好处是把复制对象的任务交个对象自己完成，不需要暴露内部状态
给客户端。

如果是Python实现的话，只需要实现`__copy__` 和 `__deepcopy__` 即可。当然也可以使用经典的
`clone`接口。

### 总结

其实这几个创造模式围绕的核心都是：面向接口编程 和 延迟创建。无论是抽象工厂、单例、原型，他们
管理依赖的基石都是通过接口，接口隐藏了细节和复杂度（比如复杂的构造过程、复杂的拷贝过程等等）。
也正是因为有了接口，我们就把创建类的任务委托给了其他对象。

## 结构模式，Structural Patterns

结构模式主要是针对如何把不同的数据（对象）放在一起。我们会分析如下设计模式：

- 组合，Composite
- 转换器，Adapter
- 代理，Proxy
- 装饰器，Decorator
- 桥接，Bridge

随着我们的分析会进一步发现，这些模式可以存在往往是因为原则1，即面向接口编程。

### 组合，Composite

在讨论创造模式的时候，我们看到很多模式对于动态语言来说显得过于啰嗦。
但是，无论在动态语言，还是静态语言中，组合模式是我认为非常有用且强大的模式。

组合模式适用于组织树状数据结构，组合模式通过结构可以让简单数据和由简单数据复合形成的
复杂结构共享同一个结构，实现“一视同仁”。

我们举个简单的例子，假设我们有两种对象：物品和盒子。盒子里面可以包含若干物品，也可以包含
更多的盒子。但是物品里面没有盒子，也就是说，物品是我们的最基对象，而盒子是复杂对象。
每一个物品都有一个价格，而盒子的价格等于其中物品价格的总和。那么，给出一个对象（盒子或
物品），我们需要计算他的价格。如何组织数据结构呢？

一种方式，我们一层一层遍历对象，判断如果是物品，提取价格，如果是盒子，进一步遍历。

另一种方法就是使用组合模式，让基本对象（物品）和复合对象（盒子）共享一个接口，这样我们
就不需要判断对象的类型，实现递归。

```python
from typing import List
from abc import abstractmethod, ABC


class ThingI(ABC):
    
    @abstractmethod
    def price(self) -> float:
        ...


class Product(ThingI):

    def __init__(self, price) -> None:
        super().__init__()
        self._price = price
    
    def price(self) -> float:
        return self._price
    
    
class Box(ThingI):
    
    def __init__(self, contents: List[ThingI]) -> None:
        # 假设没有循环出现
        super().__init__()
        self.contents = contents

    def price(self) -> float:
        sum_price = 0
        for item in self.contents:
            sum_price += item.price()
        return sum_price

def main():
    
    a = Product(1.0)
    b = Product(1.0)
    c = Box(contents=[
        Product(1.0),
        Box(
            contents=[
                Product(1.0)
            ]
        ),
        Box(
            contents=[
                a, b
            ]
        )
    ])
    
    print(f"Price of c is {c.price()}")

main()
```

如上面的例子，我们把计算和遍历对象内部状态的事情留给了对象自己，调用者完全不需要知道对象那种
类型，也无需知道内部的状态，它仅仅通过调用接口即可。这种通过接口统一不用对象的方法非常实用。
当然传统的设计模式中，复合对象（本例中的盒子）还会有一些特殊的方法，比如用来增加和减少他自己的
子对象等等。不过加入这些方法，可能会打破基本类型和复合类型的对称性，在后续的代码编写过程中
可能会造成问题。

### 转换器、桥接、装饰器、代理

这四种模式其实有类似的地方，他们都是通过在原有的对象之间增加一个兼容两边的接口，实现对不同类型
的组合。转换器与桥接的主要区别在于，转换器通常是在软件开发的后续过程中由于增加新的功能，需要
协调已经有的部分；而桥接主要是在软件设计阶段。其实某种程度上，我们的机器人例子中的组装工厂就
有点桥接的意思了。桥接主要是通过对象面A对其他的对象B的结构编程，从而解耦合A和B的具体实现。

代理和装饰器则是通过实现一个与原对象相同的接口，从而实现对原有功能的一个拓展或者更改。设计模式
里面的装饰器模式跟Python的装饰器并不是同一个事情，但是实际上实现的功能非常类似。只不过Python
的装饰器主要是针对函数的，而函数本身也确实没有类型（其实有，但是对于Python真的不重要）。

### 总结

通过上述分析，可以发现接口在组织数据结构对象和解耦合方面有奇效。依然贯彻面对接口编程的原则。

## 行为模式，Behavior Patterns

行为模式强调的是对象之间的计算和互动模式。主要涉及：

- 访问者，Visitor
- 观察者，Observer
- 命令，Command
- 迭代器，Iterator
- 备忘录，Memento
- 策略，Strategy
- 状态机，State

这类设计模式比较丰富，不同语言特性实现出来的风格迥异，但是他们蕴含的设计里面才是精华。

### 访问者，Visitor

访问者模式强调分离同一个数据对象与他的算法。经典的实现如下代码，其核心部分是 `Visitor` 这个
结构以及每一个被访问的对象的 `accept` 方法。

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Visitor(ABC):
    """
    The Visitor Interface declares a set of visiting methods that correspond to
    component classes. The signature of a visiting method allows the visitor to
    identify the exact class of the component that it's dealing with.
    """

    @abstractmethod
    def visit_concrete_component_a(self, element: ConcreteComponentA) -> None:
        pass

    @abstractmethod
    def visit_concrete_component_b(self, element: ConcreteComponentB) -> None:
        pass


class Component(ABC):
    """
    The Component interface declares an `accept` method that should take the
    base visitor interface as an argument.
    """

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass

class ConcreteComponentA(Component):
    """
    Each Concrete Component must implement the `accept` method in such a way
    that it calls the visitor's method corresponding to the component's class.
    """

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_concrete_component_a(self)

    def exclusive_method_of_concrete_component_a(self) -> str:
        """ Concrete Components may have special methods that don't exist in their
        base class or interface. The Visitor is still able to use these methods
        since it's aware of the component's concrete class.
        """

        return "A"


class ConcreteComponentB(Component):
    """ Same here: visitConcreteComponentB => ConcreteComponentB """

    def accept(self, visitor: Visitor):
        visitor.visit_concrete_component_b(self)

    def special_method_of_concrete_component_b(self) -> str:
        return "B"


class ConcreteVisitor1(Visitor):
    def visit_concrete_component_a(self, element) -> None:
        print(f"{element.exclusive_method_of_concrete_component_a()} + ConcreteVisitor1")

    def visit_concrete_component_b(self, element) -> None:
        print(f"{element.special_method_of_concrete_component_b()} + ConcreteVisitor1")


class ConcreteVisitor2(Visitor):
    def visit_concrete_component_a(self, element) -> None:
        print(f"{element.exclusive_method_of_concrete_component_a()} + ConcreteVisitor2")

    def visit_concrete_component_b(self, element) -> None:
        print(f"{element.special_method_of_concrete_component_b()} + ConcreteVisitor2")

def client_code(components: List[Component], visitor: Visitor) -> None:
    """
    The client code can run visitor operations over any set of elements without
    figuring out their concrete classes. The accept operation directs a call to
    the appropriate operation in the visitor object.
    """

    # ...
    for component in components:
        component.accept(visitor)
    # ...
```

### 观察者，Observer

这种设计模式可以说非常常见了，观察者也就是我们经常听到的广播订阅模式。这种模式如今已经走出了
设计模式的范畴，在架构领域也是经常见到，比如我们常见的Kafka就是这种设计模式实现的中间件。

同时，与访问者对比，观察者会被动得到通知，而访问者需要主动要求 (调用`accept`)。

经典的实现如下：

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
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
```


### 命令，Command

命令模式在如今的软件工程中也非常常见，它其实是一种对象之间的通讯方式，命令模式会把一个请求
转换成包含完成这个命令的信息的独立对象，这个命令对象随后可以被发送给命令的执行对象执行。
从而实现了发送者和接受者的解耦合。看起来与观察者有一点类似，命令的执行者可以算是某种命令的
观察者。

```python
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
```

### 迭代器，Iterator

迭代器是关于如何遍历数据结构的模式。比如一个树结构，我们可以通过定义迭代器接口方法：`iterator` 来抽象不同的遍历风格，比如深度优先、广度优先等等。

### 备忘录，Memento

备忘录是一种在不打破对象封装的前提下，对对象进行快照的方法，通过快照我们可以方便的进行历史重现。其核心在于把管理快照的功能交给其他对象。在Python中快照可以通过不同的序列化实现。

### 策略，Strategy

策略模式其实就是为算法定义一个接口，从而实现随意插入任意具体算法的模式。可以参考机器人的例子。
抽象工厂可以理解成某个工厂算法。

### 状态机，State

状态机也是非常常见的设计模式，也就是一个对象的行为，取决于它内部的状态；而他对事件的相应，也会
影响他内部的状态。我认为是一种与组合模式同样影响深远的模式。状态机会把这些复杂度封装在对象内部
而不会让客户端通过一些if语句来控制。同样，这也是一种责任交付。

```python
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
```

## 总结

可以看出，设计模式主要使用的技巧就是：

- 面对接口编程
- 延迟执行
- 依赖注入
- 组合 而不是 继承

在上面的例子中，所有的继承都紧紧是接口的一种实现，并不是真正意义的共享状态，而是共享合同。
这种共享接口让程序变更加容易拓展。依赖注入可以看成某种延迟执行。

当然，不同的语言特性会让这些模式实现看起来非常不一样，比如采用鸭子类型的语言，Python或者Go，
很多继承是不需要的，我们只需要duck type接口的方法即可。

## 参考

- https://refactoring.guru/design-patterns
- https://github.com/faif/python-patterns