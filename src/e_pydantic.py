from enum import Enum
from pydantic import BaseModel, validator, ValidationError, Extra, validate_arguments

class StockId(str):
    ...

class Region(str, Enum):
    US = "US"
    CN = "CN"
    PE = "PE"
    JP = "JP"


class Stock(BaseModel, extra=Extra.forbid):
    
    id: StockId
    name: str 
    region: Region

    @validator("id")
    def no_space(cls, v):
        if ' ' in v:
            raise ValueError("No space is allowed in id")
        return v


s1 = Stock(id="A1", name="Apple Inc.", region=Region.US)
d1 = s1.dict()
j1 = s1.json()

print(f"{s1}")
print(f"{s1.dict()}")
print(f"{s1.json()}")
print(f"{Stock.parse_raw(j1)}")
print(f"{Stock(**d1)}")
print(f"{s1.schema()}")


try:
    s2 = Stock(id="A 2", name="Apple Inc.", region=Region.US)
except ValidationError as e:
    print(e)

    
try:
    s3 = Stock(id="A2", name="Apple Inc.", region=Region.US, ran=22)
except ValidationError as e:
    print(e)
    

@validate_arguments
def repeat(s: str, count: int, *, separator: bytes=b'') -> bytes:
    b = s.encode()
    return separator.join(b for _ in range(count))

a = repeat('hello', 3)
print(a)
#> b'hellohellohello'

b = repeat('x', '4', separator=' ')
print(b)
#> b'x x x x'

try:
    c = repeat('hello', 'wrong')
except ValidationError as exc:
    print(exc)
    """
    1 validation error for Repeat
    count
      value is not a valid integer (type=type_error.integer)
    """