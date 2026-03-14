import pytest

from src.binutils import (
    invert_bit_at,
    invert_sign,
    invert_reversed_bin,
    invert_bit
)
from src.consts import WORD_SIZE

@pytest.mark.parametrize("initial_list, index, expected_list", [
    ([0, 0, 0, 0], 0, [1, 0, 0, 0]),  
    ([1, 1, 1, 1], 2, [1, 1, 0, 1]),  
    ([0, 1, 0, 1], 3, [0, 1, 0, 0]),  
])
def test_invert_bit_at(initial_list, index, expected_list):
    """Проверка инвертирования конкретного бита 'in-place' (изменение самого объекта)."""
    lst = initial_list.copy()
    

    assert invert_bit_at(index, lst) is None
    assert lst == expected_list


# --- Тесты для invert_sign ---

def test_invert_sign():
    """Проверка инверсии только знакового бита (нулевой индекс) с сохранением оригинала."""
    original = [0] * WORD_SIZE
    expected = [1] + [0] * (WORD_SIZE - 1)
    
    result = invert_sign(original)
    
    assert result == expected
    assert original == [0] * WORD_SIZE

def test_invert_sign_from_one():
    """Дополнительная проверка смены знака с минуса (1) на плюс (0)."""
    original = [1] + [0] * (WORD_SIZE - 1)
    expected = [0] * WORD_SIZE
    
    assert invert_sign(original) == expected


def test_invert_reversed_bin_from_zeros():
    """Проверка инвертирования мантиссы: знаковый бит не меняется, остальные инвертируются."""
    original = [0] * WORD_SIZE
    expected = [0] + [1] * (WORD_SIZE - 1)
    
    result = invert_reversed_bin(original)
    
    assert result == expected
    assert original == [0] * WORD_SIZE # Оригинал не должен пострадать

def test_invert_reversed_bin_from_ones():
    """Проверка обратного преобразования мантиссы (единицы в нули)."""
    original = [1] * WORD_SIZE
    expected = [1] + [0] * (WORD_SIZE - 1)
    
    result = invert_reversed_bin(original)
    
    assert result == expected



@pytest.mark.parametrize("bit, expected", [
    (0, 1),
    (1, 0),
])
def test_invert_bit(bit, expected):
    """Проверка инверсии одиночного бита."""
    assert invert_bit(bit) == expected