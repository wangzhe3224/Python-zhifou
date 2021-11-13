from dataclasses import dataclass
import pytest
import logging

logging.basicConfig(level=logging.INFO)

def function_prints():
    print("Catch!")

def function_log():
    logging.getLogger().info("Catch me!")

# https://docs.pytest.org/en/6.2.x/fixture.html
# 基础测试
def test_basic():
    # call some function, get some results, and assert
    assert 1 == 1
    # assert 1 == 2

# Side effects
def test_exp():
    # raise KeyError("I am catched by pytest")
    with pytest.raises(KeyError):
        # 希望异常的函数调用放在这里
        raise KeyError("I am catched by pytest")
    # with pytest.raises(IndexError):
    #     raise KeyError("Not catched")

def test_print_message(capsys):
    function_prints()
    captured = capsys.readouterr()
    assert captured.out == "Catch!\n"

def test_log_content(caplog):
    with caplog.at_level(logging.DEBUG):
        function_log()
    assert 'Catch me!' in caplog.text   

# fixtures
@dataclass
class Fruit:
    name: str

@pytest.fixture
def my_fruit():
    return Fruit("apple")

@pytest.fixture
def fruit_basket(my_fruit):
    return [Fruit("banana"), my_fruit]

def test_my_fruit_in_basket(my_fruit, fruit_basket):
    assert len(fruit_basket) == 2  # < 注意这 没有被其他的测试影响
    assert my_fruit in fruit_basket

def test_modify(fruit_basket):
    # Act
    fruit_basket.append(Fruit("x"))
    # Assert
    assert fruit_basket[-1] == Fruit("x")

# @pytest.fixture(autouse=True)
# def append_first(order, first_entry):
#     return order.append(first_entry)

# marks
@pytest.mark.parametrize(
    "input1, input2, expected_out",
    [
        ('a', 'b', 'ab'),
        ('', 'b', 'b'),
    ],
    ids=[
        'a + b = ab',
        '_ + b = b',
    ]
)
def test_params_marks(input1, input2, expected_out):
    res = input1 + input2
    assert res == expected_out


@pytest.mark.skip()
def test_pass_marks():
    # will fail, fix later
    with pytest.raises(IndexError):
        raise KeyError("Not catched")