from src.consts import WORD_SIZE, ONE
from src.binops import add_binary
from src.binutils import invert_bit_at

def dec_to_direct_bin(num: int) -> list[int]:
    """Перевод из десятичного в прямой код."""
    bin_p = [0] * WORD_SIZE
    if num < 0:
        bin_p[0] = 1
    temp = abs(num)
    i = WORD_SIZE - 1
    while temp > 0:
        bin_p[i] = temp % 2
        temp //= 2
        i -= 1
    return bin_p

def dec_to_reverse_bin(num: int) -> list[int]:
    """Перевод из десятичного в обратный код."""
    bin_p = dec_to_direct_bin(num)
    if bin_p[0] == 1:
        for i in range(WORD_SIZE - 1, 0, -1):
            invert_bit_at(i, bin_p)
    return bin_p

def dec_to_twos_complement(num: int) -> list[int]:
    """Перевод из десятичного в дополнительный код."""
    bin_rev = dec_to_reverse_bin(num)
    if bin_rev[0] == 1:
        return add_binary(bin_rev, ONE)
    return bin_rev
    
def direct_bin_to_dec(binary_array: list[int]) -> int:
    """Из прямого кода в десятичное."""
    sign = binary_array[0]
    value = sum(bit * (2 ** i) for i, bit in enumerate(reversed(binary_array[1:])))
    return -value if sign == 1 else value

def reverse_bin_to_dec(binary_array: list[int]) -> int:
    """Из обратного кода в десятичное."""
    if binary_array[0] == 0:
        return direct_bin_to_dec(binary_array)
    
    inverted_bits = [1 - bit for bit in binary_array]
    value = sum(bit * (2 ** i) for i, bit in enumerate(reversed(inverted_bits[1:])))
    return -value

def twos_complement_to_dec(binary_array: list[int]) -> int:
    """Из дополнительного кода в десятичное."""
    n = len(binary_array)
    value = -binary_array[0] * (2 ** (n - 1))
    
    for i in range(1, n):
        power = n - 1 - i
        value += binary_array[i] * (2 ** power)
        
    return value