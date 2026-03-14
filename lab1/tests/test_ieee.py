import pytest
from src.ieee import (
    ieee_to_float,
    float_to_ieee,
    unpack_parts,
    pack_parts,
    multiply_ieee,
    divide_ieee,
    add_ieee,
    sub_ieee
)

ZERO_BITS = [0] * 32
NEG_ZERO_BITS = [1] + [0] * 31
ONE_BITS = [0, 0, 1, 1, 1, 1, 1, 1, 1] + [0] * 23          # 1.0
NEG_ONE_BITS = [1, 0, 1, 1, 1, 1, 1, 1, 1] + [0] * 23      # -1.0
TWO_BITS = [0, 1, 0, 0, 0, 0, 0, 0, 0] + [0] * 23          # 2.0
HALF_BITS = [0, 0, 1, 1, 1, 1, 1, 1, 0] + [0] * 23         # 0.5
ONE_POINT_FIVE = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1] + [0] * 22 # 1.5



def test_ieee_to_float_invalid_length():
    """Проверка генерации ошибки при неверной длине массива."""
    with pytest.raises(ValueError, match="Массив должен содержать ровно 32 бита"):
        ieee_to_float([0] * 31)

@pytest.mark.parametrize("bits, expected", [
    (ZERO_BITS, 0.0),
    (NEG_ZERO_BITS, -0.0),
    (ONE_BITS, 1.0),
    (NEG_ONE_BITS, -1.0),
    (TWO_BITS, 2.0),
    (HALF_BITS, 0.5),
    (ONE_POINT_FIVE, 1.5),
])

def test_ieee_to_float(bits, expected):
    """Проверка перевода 32-битного массива в float."""
    assert ieee_to_float(bits) == expected

@pytest.mark.parametrize("val, expected", [
    (0.0, ZERO_BITS),
    (-0.0, NEG_ZERO_BITS),
    (1.0, ONE_BITS),
    (-1.0, NEG_ONE_BITS),
    (2.0, TWO_BITS),          
    (0.5, HALF_BITS),         
    (1.5, ONE_POINT_FIVE),
])
def test_float_to_ieee(val, expected):
    """Проверка перевода float в 32-битный массив IEEE 754."""
    assert float_to_ieee(val) == expected


def test_pack_unpack_parts():
    """Проверка извлечения и упаковки знака, экспоненты и мантиссы."""
    sign, exp, mantissa = unpack_parts(ONE_POINT_FIVE)
    assert sign == 0
    assert exp == 127
    expected_mantissa = (1 << 23) | (1 << 22)
    assert mantissa == expected_mantissa
    
    assert pack_parts(sign, exp, mantissa) == ONE_POINT_FIVE


def test_multiply_ieee():
    """Проверка умножения IEEE 754 чисел."""
    assert multiply_ieee(ZERO_BITS, ONE_BITS) == [0] * 32
    
    res = multiply_ieee(ONE_POINT_FIVE, TWO_BITS)
    assert ieee_to_float(res) == 3.0
    
    assert multiply_ieee(NEG_ONE_BITS, NEG_ONE_BITS) == ONE_BITS
    
    res2 = multiply_ieee(ONE_POINT_FIVE, ONE_POINT_FIVE)
    assert ieee_to_float(res2) == 2.25


def test_divide_ieee():
    """Проверка деления IEEE 754 чисел."""
    with pytest.raises(ZeroDivisionError, match="Division by zero"):
        divide_ieee(ONE_BITS, ZERO_BITS)
        
    assert divide_ieee(ZERO_BITS, ONE_BITS) == [0] * 32
    
    res1 = divide_ieee(ONE_BITS, TWO_BITS)
    assert ieee_to_float(res1) == 0.5
    
    res2 = divide_ieee(TWO_BITS, ONE_POINT_FIVE)
    assert round(ieee_to_float(res2), 5) == round(2.0 / 1.5, 5)


def test_add_ieee():
    """Проверка сложения чисел с плавающей точкой (все пограничные ветки)."""
    assert add_ieee(ZERO_BITS, ONE_BITS) == ONE_BITS
    assert add_ieee(ONE_BITS, ZERO_BITS) == ONE_BITS
    
    large_num = float_to_ieee(2**30)
    assert add_ieee(large_num, ONE_BITS) == large_num 
    
    res_add1 = add_ieee(ONE_POINT_FIVE, HALF_BITS)
    assert ieee_to_float(res_add1) == 2.0
    
    neg_half = float_to_ieee(-0.5)
    res_add2 = add_ieee(ONE_POINT_FIVE, neg_half)
    assert ieee_to_float(res_add2) == 1.0
    
    res_add3 = add_ieee(HALF_BITS, float_to_ieee(-1.5))
    assert ieee_to_float(res_add3) == -1.0
    
    assert add_ieee(ONE_BITS, NEG_ONE_BITS) == ZERO_BITS

    res_swap = add_ieee(HALF_BITS, ONE_BITS) # 0.5 + 1.0
    assert ieee_to_float(res_swap) == 1.5


def test_sub_ieee():
    """Проверка вычитания через инверсию знака второго аргумента."""
    res = sub_ieee(ONE_POINT_FIVE, HALF_BITS)
    assert ieee_to_float(res) == 1.0
    
    res2 = sub_ieee(ONE_BITS, NEG_ONE_BITS)
    assert ieee_to_float(res2) == 2.0