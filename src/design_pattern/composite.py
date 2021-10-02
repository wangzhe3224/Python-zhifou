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