import pytest

from src.transformInt import (
    dec_to_direct_bin,
    dec_to_reverse_bin,
    dec_to_twos_complement,
    direct_bin_to_dec,
    reverse_bin_to_dec,
    twos_complement_to_dec
)
from src.consts import WORD_SIZE

def pad_zeros(sign: int, bits: list[int]) -> list[int]:
    """Создает массив с нулями между битом знака и значащими битами."""
    return [sign] + [0] * (WORD_SIZE - 1 - len(bits)) + bits

def pad_ones(sign: int, bits: list[int]) -> list[int]:
    """Создает массив с единицами между битом знака и значащими битами (для отрицательных чисел)."""
    return [sign] + [1] * (WORD_SIZE - 1 - len(bits)) + bits

@pytest.mark.parametrize("num, expected", [
    (0, pad_zeros(0, [])),
    (5, pad_zeros(0, [1, 0, 1])),
    (-5, pad_zeros(1, [1, 0, 1])),
    (12, pad_zeros(0, [1, 1, 0, 0])),
    (-12, pad_zeros(1, [1, 1, 0, 0])),
])
def test_dec_to_direct_bin(num, expected):
    """Проверка перевода десятичного числа в прямой код (знак + модуль)."""
    assert dec_to_direct_bin(num) == expected


@pytest.mark.parametrize("num, expected", [
    (0, pad_zeros(0, [])),
    (5, pad_zeros(0, [1, 0, 1])),        
    (-5, pad_ones(1, [0, 1, 0])),        
    (-12, pad_ones(1, [0, 0, 1, 1])),
])
def test_dec_to_reverse_bin(num, expected):
    """Проверка перевода в обратный код (инверсия мантиссы для отрицательных)."""
    assert dec_to_reverse_bin(num) == expected


@pytest.mark.parametrize("num, expected", [
    (0, pad_zeros(0, [])),
    (5, pad_zeros(0, [1, 0, 1])),        
    (-5, pad_ones(1, [0, 1, 1])),        
    (-12, pad_ones(1, [0, 1, 0, 0])),
])
def test_dec_to_twos_complement(num, expected):
    """Проверка перевода в дополнительный код."""
    assert dec_to_twos_complement(num) == expected


@pytest.mark.parametrize("binary_array, expected", [
    (pad_zeros(0, []), 0),
    (pad_zeros(0, [1, 0, 1]), 5),
    (pad_zeros(1, [1, 0, 1]), -5),
])
def test_direct_bin_to_dec(binary_array, expected):
    """Проверка перевода прямого кода обратно в десятичное число."""
    assert direct_bin_to_dec(binary_array) == expected


@pytest.mark.parametrize("binary_array, expected", [
    (pad_zeros(0, [1, 0, 1]), 5),        
    (pad_ones(1, [0, 1, 0]), -5),        
    (pad_zeros(0, []), 0),
])
def test_reverse_bin_to_dec(binary_array, expected):
    """Проверка перевода обратного кода в десятичное число."""
    assert reverse_bin_to_dec(binary_array) == expected


@pytest.mark.parametrize("binary_array, expected", [
    (pad_zeros(0, [1, 0, 1]), 5),        
    (pad_ones(1, [0, 1, 1]), -5),        
    (pad_zeros(0, []), 0),
    ([1] + [0] * (WORD_SIZE - 1), -(2 ** (WORD_SIZE - 1))), 
])
def test_twos_complement_to_dec(binary_array, expected):
    """Проверка математически корректного перевода дополнительного кода с учетом веса знакового бита."""
    assert twos_complement_to_dec(binary_array) == expected