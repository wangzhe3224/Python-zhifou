
def stateful(state: int):
    
    def _inner(new: int):
        nonlocal state
        state += new

        return state
    
    return _inner

    
class Stateful:
    
    def __init__(self, state: int) -> None:
        self._state = state
        
    def __call__(self, new: int) -> int:
        self._state += new
        return self._state


if __name__ == "__main__":
    
    state = -1
    f = stateful(10)
    print(f(1))
    print(state)
    print(f(1))
    print(state)

    # 闭包
    print(f)
    print(f.__closure__)
    print(f.__closure__[0].cell_contents)