from dataclasses import dataclass
# https://www.python.org/dev/peps/pep-0557/#rationale
# https://docs.python.org/3/library/dataclasses.html

# 为什么需要 `dataclass`

class InventoryItem:
    
    def __init__(self, name: str, unit_price: float, quantity_on_hand: int = 0, category: str = 'default') -> None:
        self.name = name
        self.unit_price = unit_price
        self.quantity_on_hand = quantity_on_hand
        self.category = category

    def __repr__(self):
        return f'InventoryItem(name={self.name!r}, unit_price={self.unit_price!r}, \
                 quantity_on_hand={self.quantity_on_hand!r}, category={self.category!r})'

    def __gt__(self, other):
        if other.__class__ is self.__class__:
            return (self.name, self.unit_price, self.quantity_on_hand) > (other.name, other.unit_price, other.quantity_on_hand)
        return NotImplemented      
    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.name, self.unit_price, self.quantity_on_hand) == (other.name, other.unit_price, other.quantity_on_hand)
        return NotImplemented
    # def __ne__(self, other):
    #     if other.__class__ is self.__class__:
    #         return (self.name, self.unit_price, self.quantity_on_hand) != (other.name, other.unit_price, other.quantity_on_hand)
    #     return NotImplemented
    # def __lt__(self, other):
    #     if other.__class__ is self.__class__:
    #         return (self.name, self.unit_price, self.quantity_on_hand) < (other.name, other.unit_price, other.quantity_on_hand)
    #     return NotImplemented
    # def __le__(self, other):
    #     if other.__class__ is self.__class__:
    #         return (self.name, self.unit_price, self.quantity_on_hand) <= (other.name, other.unit_price, other.quantity_on_hand)
    #     return NotImplemented


# @dataclass(init=True, repr=True, eq=True, order=True, frozen=True)
@dataclass(order=True)
class InventoryItemBetter:
    name: str
    unit_price: float 
    quantity_on_hand: int = 0

@dataclass
class Something:

    x: int = 1
    y: int = 1
    something: str = "111"

@dataclass
class SomethingSlot:
    __slots__ = ['something', 'x', 'y']
    x: int = 1
    y: int = 1
    something: str = "111"


if __name__ == '__main__':
    s = Something(something='11', x=1, y=1)
    sslot = SomethingSlot(something='11', x=1, y=1)
    
    from pympler import asizeof
    print(f"Something: {asizeof.asizeof(s)}")
    print(f"SomethingSlot: {asizeof.asizeof(sslot)}")
    
    # o1 = InventoryItem('ItemA', unit_price=10, quantity_on_hand=100)
    # o2 = InventoryItem('ItemA', unit_price=10, quantity_on_hand=100)
    # o1 = InventoryItemBetter('ItemA', unit_price=10, quantity_on_hand=100)
    # o2 = InventoryItemBetter('ItemA', unit_price=10, quantity_on_hand=100)
    # o3 = Something('ItemA', unit_price=10, quantity_on_hand=100)
    # print(o3)
    # print(f"{o1 > o2 = }")
    # print(f"{o1 == o2 = }")
    # print(f"{o1 <= o2 = }")