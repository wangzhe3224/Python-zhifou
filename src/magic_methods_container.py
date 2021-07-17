class MyContainer:

    def __init__(self) -> None:
        self._dict = {}

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __len__(self):
        return len(self._dict)

    def __delitem__(self, key):
        del self._dict[key]

    def __iter__(self):
        return iter(self._dict)

if __name__ == '__main__':

    my = MyContainer()

    my['k1'] = 1

    print(f'{my["k1"] = }')

    print(f'{len(my) = }' )
    
    del my['k1']

    print(f'for ... in ...')
    my['k1'] = 1
    my['k2'] = 2
    for key in my:
        print(key)
        print(f'{my[key] = }')