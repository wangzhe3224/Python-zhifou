import datetime
import timeit


def equals_debugging():
    str_value = "一只 åß∂ƒµ🐶"
    num_value = 123
    print(f'the value is {str_value}')
    print(f'{num_value = }')
    print(f"num_value = {num_value}")
    print(f'debug : {num_value % 2 = }')


def conversions():
    str_value = "一只狗 🐶"
    print(f'{str_value}')  # __str__
    print(f'{str_value!s}')  # __str__
    print(f'{str_value!r}')  # !r __repr__


class MyClass:
    def __format__(self, format_spec) -> str:
        print(f'MyClass __format__ called with {format_spec=!r}')
        return "MyClass() ????"
    
    def __repr__(self) -> str:
        return "MyClass repr."
    
    def __str__(self) -> str:
        return "MyClass str" 


def formatting():
    num_value = 123.456
    now = datetime.datetime.utcnow()
    m = MyClass()
    print(m)
    print(f'{m!s}')
    print(f'{m!r}')
    print(f'{now=:%Y-%m-%d}')
    print(f'{num_value:.2f}')
    print(f'{MyClass():blah blah %%MYFORMAT%%}')

    nested_format = ".2f"
    print(f'{num_value:{nested_format}}')


def s_speed():
    timeit.timeit("""name="Saral"
    age = 30
    '%s is %s.' % (name, age)""", number=1000000)


def f_speed():
    timeit.timeit("""name="Saral"
    age = 30
    f'{name} is {age}.'""", number=1000000)


def main():
    # equals_debugging()
    # conversions()
    formatting()


if __name__ == '__main__':
    main()
