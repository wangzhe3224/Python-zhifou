class MyContainer:

    def __init__(self) -> None:
        self._dict = {}

    def __setitem__(self, key, value):
        # my[k1] = 1
        self._dict[key] = value

    def __getitem__(self, key):
        # my[k1]
        return self._dict[key]

    def __len__(self):
        # len(my)
        return len(self._dict)

    def __delitem__(self, key):
        # del my[k1]
        del self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __contains__(self, item):
        # something IN my
        return item in self._dict

if __name__ == '__main__':

    my = MyContainer()

    my['k1'] = 1
    my['k2'] = 2

    print(f'{my["k1"] = }')

    print(f'{len(my) = }' )
    
    del my['k1']

    print(f'for ... in ...')
    my['k1'] = 1
    my['k2'] = 2
    for key in my:
        print(key)
        print(f'{my[key] = }')

    print(f"{'k1' in my = }")
    print(f"{'k3' in my = }")