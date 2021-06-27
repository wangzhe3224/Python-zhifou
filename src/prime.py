import math


def check_prime(number):
    sqrt = math.sqrt(number)
    for i in range(2, int(sqrt)+1):
        if (number / i).is_integer():
            return False
    
    return True


def check_prime(number):
    sqrt_number = math.sqrt(number) 
    numbers = range(2, int(sqrt_number)+1) 
    for i in range(0, len(numbers), 5):
        # the following line is not valid Python code
        result = (number / numbers[i:(i + 5)]).is_integer() 
        if any(result):
            return False

    return True


def search_unknown1(haystack, needle):
    return any((item == needle for item in haystack))


def search_unknown2(haystack, needle):
    return any([item == needle for item in haystack])

print(check_prime(12))
