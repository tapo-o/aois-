import pytest

# Замените dcb5421 на bcd5421, если имя файла в src отличается
from src.bcd5421 import (
    encode_digit_5421,
    decode_digit_5421,
    number_to_bcd_array,
    add_bcd_5421
)

@pytest.mark.parametrize("digit, expected_bits", [
    (0, [0, 0, 0, 0]),
    (1, [0, 0, 0, 1]),
    (2, [0, 0, 1, 0]),
    (3, [0, 0, 1, 1]),
    (4, [0, 1, 0, 0]),
    (5, [1, 0, 0, 0]),
    (6, [1, 0, 0, 1]),
    (7, [1, 0, 1, 0]),
    (8, [1, 0, 1, 1]),
    (9, [1, 1, 0, 0]),
])
def test_encode_digit_5421(digit, expected_bits):
    """Проверка кодирования всех десятичных цифр (0-9) в 5421 BCD."""
    assert encode_digit_5421(digit) == expected_bits


@pytest.mark.parametrize("bits, expected_digit", [
    ([0, 0, 0, 0], 0),
    ([0, 0, 0, 1], 1),
    ([0, 0, 1, 0], 2),
    ([0, 0, 1, 1], 3),
    ([0, 1, 0, 0], 4),
    ([1, 0, 0, 0], 5),
    ([1, 0, 0, 1], 6),
    ([1, 0, 1, 0], 7),
    ([1, 0, 1, 1], 8),
    ([1, 1, 0, 0], 9),
])
def test_decode_digit_5421(bits, expected_digit):
    """Проверка декодирования 4-битных списков обратно в цифры."""
    assert decode_digit_5421(bits) == expected_digit

@pytest.mark.parametrize("number, expected_array", [
    (0,   [[0, 0, 0, 0]]),
    (5,   [[1, 0, 0, 0]]),
    (42,  [[0, 1, 0, 0], [0, 0, 1, 0]]),
    (159, [[0, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0]]),
])
def test_number_to_bcd_array(number, expected_array):
    """Проверка разбиения многозначных чисел (и нуля) на массив нибблов 5421 BCD."""
    assert number_to_bcd_array(number) == expected_array

@pytest.mark.parametrize("num1, num2, expected_sum", [
    (0, 0, 0),             
    (2, 3, 5),             
    (8, 9, 17),            
    (42, 15, 57),          
    (99, 1, 100),          
    (1234, 5678, 6912),    
])
def test_add_bcd_5421(num1, num2, expected_sum):
    """Проверка математического сложения BCD массивов."""
    bcd1 = number_to_bcd_array(num1)
    bcd2 = number_to_bcd_array(num2)
    expected_bcd = number_to_bcd_array(expected_sum)

    assert add_bcd_5421(bcd1, bcd2) == expected_bcd