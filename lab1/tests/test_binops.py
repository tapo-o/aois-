import pytest
from unittest.mock import patch

from src.binops import add_binary, subtract, multiply, divide
from src.consts import WORD_SIZE, ONE

def pad(bits: list[int], length: int = WORD_SIZE) -> list[int]:
    """Дополняет массив нулями слева до нужной длины (или обрезает лишнее)."""
    if len(bits) >= length:
        return bits[-length:]
    return [0] * (length - len(bits)) + bits

def make_bin(sign: int, val: list[int]) -> list[int]:
    """Создает бинарное число с битом знака и дополнением мантиссы до WORD_SIZE - 1."""
    return [sign] + pad(val, WORD_SIZE - 1)


@pytest.mark.parametrize("val1, val2, expected_val", [
    ([0], [0], [0]),
    ([1], [0], [1]),
    ([1], [1], [1, 0]),                
    ([1, 0, 1], [1, 1], [1, 0, 0, 0]), 
])
def test_add_binary(val1, val2, expected_val):
    """Проверка корректного побитового сложения с учетом переноса."""
    bin1 = pad(val1)
    bin2 = pad(val2)
    expected = pad(expected_val)
    assert add_binary(bin1, bin2) == expected

def test_add_binary_overflow():
    """Проверка отбрасывания лишнего бита при переполнении разрядной сетки."""
    bin1 = [1] * WORD_SIZE
    bin2 = pad([1])
    expected = [0] * WORD_SIZE
    assert add_binary(bin1, bin2) == expected

@patch('src.binops.add_binary')
@patch('src.binops.invert_reversed_bin')
@patch('src.binops.invert_sign')
def test_subtract(mock_invert_sign, mock_inv_rev, mock_add):
    """
    Тестируем subtract с моками, чтобы изолировать логику binops
    от реальной реализации в binutils.py.
    """
    mock_invert_sign.return_value = [2]
    mock_inv_rev.return_value = [3]
    
    mock_add.side_effect = [[4], [5]] 
    
    bin1 = [1, 0]
    bin2 = [0, 1]
    
    result = subtract(bin1, bin2)
    
    mock_invert_sign.assert_called_once_with(bin2)
    mock_inv_rev.assert_called_once_with([2])
    assert mock_add.call_count == 2
    assert result == [5]

@pytest.mark.parametrize("sign1, val1, sign2, val2, exp_sign, exp_val", [
    (0, [0], 0, [0], 0, [0]),             
    (0, [1, 1], 0, [1, 0], 0, [1, 1, 0]), 
    (1, [1, 1], 0, [1, 0], 1, [1, 1, 0]), 
    (1, [1, 0], 1, [1, 0], 0, [1, 0, 0]), 
    (0, [1, 1, 1], 0, [1], 0, [1, 1, 1]), 
])
def test_multiply(sign1, val1, sign2, val2, exp_sign, exp_val):
    """Проверка умножения, включая вычисление бита знака и побитовое перемножение мантисс."""
    bin1 = make_bin(sign1, val1)
    bin2 = make_bin(sign2, val2)
    expected = make_bin(exp_sign, exp_val)
    
    assert multiply(bin1, bin2) == expected


@pytest.mark.parametrize("sign1, val1, sign2, val2, exp_sign, exp_int, exp_frac", [
    (0, [0], 0, [1, 0], 0, [0], [0]),                     
    (0, [1, 1, 0], 0, [1, 0], 0, [1, 1], [0]),            
    (1, [1, 0, 1], 0, [1, 0], 1, [1, 0], [1, 0]),         
    (0, [1], 0, [1, 0, 0], 0, [0], [0, 1]),               
    (1, [1, 0, 0], 1, [1, 0], 0, [1, 0], [0]),            
])
def test_divide(sign1, val1, sign2, val2, exp_sign, exp_int, exp_frac):
    """Проверка деления: логика знаков, выделение целой и вычисление дробной части."""
    bin1 = make_bin(sign1, val1)
    bin2 = make_bin(sign2, val2)
    
    expected_int = pad(exp_int, WORD_SIZE)
    
    expected_frac = exp_frac + [0] * (WORD_SIZE - len(exp_frac))
    expected_frac = expected_frac[:WORD_SIZE]
    
    sign, int_part, frac_part = divide(bin1, bin2)
    
    assert sign == exp_sign
    assert int_part == expected_int
    assert frac_part == expected_frac

def test_divide_by_zero():
    """Проверка обработки исключения при попытке деления на массив из нулей."""
    bin1 = make_bin(0, [1])
    bin2 = [0] * WORD_SIZE
    
    with pytest.raises(ValueError, match="Деление на ноль"):
        divide(bin1, bin2)