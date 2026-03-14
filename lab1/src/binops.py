from src.consts import WORD_SIZE, ONE
from src.binutils import invert_sign, invert_reversed_bin

def add_binary(bin1: list[int], bin2: list[int]) -> list[int]:
    """Сложение двух бинарных массивов."""
    result = [0] * WORD_SIZE
    carry = 0
    for i in range(WORD_SIZE - 1, -1, -1):
        total = bin1[i] + bin2[i] + carry
        result[i] = total % 2
        carry = total // 2
    return result

def subtract(bin1: list[int], bin2: list[int]) -> list[int]:
    """Вычитание бинарных массивов через дополнительный код."""
    bin2_inverted = invert_sign(bin2.copy())
    bin2_inverted = invert_reversed_bin(bin2_inverted)
    bin2_inverted = add_binary(bin2_inverted, ONE)
    return add_binary(bin1, bin2_inverted)

def multiply(bin1: list[int], bin2: list[int]) -> list[int]:
    """Умножение бинарных массивов."""
    sign = bin1[0] ^ bin2[0]
    m1 = bin1[1:]
    m2 = bin2[1:]

    temp = [0] * (len(m1) + len(m2))
    
    for i in range(len(m2) - 1, -1, -1):
        if m2[i] == 1:
            carry = 0
            for j in range(len(m1) - 1, -1, -1):
                idx = i + j + 1
                total_sum = temp[idx] + m1[j] + carry
                temp[idx] = total_sum % 2
                carry = total_sum // 2
            temp[i] += carry

    cutbin = temp[-(WORD_SIZE - 1):]
    return [sign] + cutbin

def divide(bin1: list[int], bin2: list[int]) -> tuple[int, list[int], list[int]]:
    """Деление двух чисел в прямом коде с фиксированной точкой."""
    if all(x == 0 for x in bin2):
        raise ValueError("Деление на ноль")

    sign = bin1[0] ^ bin2[0]
    
    num_a = int(''.join(map(str, bin1[1:])), 2)
    num_b = int(''.join(map(str, bin2[1:])), 2)

    if num_a == 0:
        return sign, [0] * WORD_SIZE, [0] * WORD_SIZE

    integer_part_val = num_a // num_b
    remainder = num_a % num_b

    fraction_bits = []
    for _ in range(WORD_SIZE):
        remainder *= 2
        bit = 1 if remainder >= num_b else 0
        fraction_bits.append(bit)
        if bit:
            remainder -= num_b

    integer_bin = bin(integer_part_val)[2:].zfill(WORD_SIZE)[-WORD_SIZE:]
    integer_part = [int(bit) for bit in integer_bin]
    fraction_part = fraction_bits[:WORD_SIZE]

    return sign, integer_part, fraction_part