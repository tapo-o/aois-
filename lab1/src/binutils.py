from src.consts import WORD_SIZE

def invert_bit_at(index: int, binary_list: list[int]) -> None:
    """Инвертирует бит по указанному индексу in-place."""
    binary_list[index] = 1 if binary_list[index] == 0 else 0

def invert_sign(binary_list: list[int]) -> list[int]:
    """Инвертирует знаковый бит (индекс 0)."""
    out = binary_list.copy()
    invert_bit_at(0, out)
    return out

def invert_reversed_bin(binary_list: list[int]) -> list[int]:
    """Инвертирует все биты, кроме знакового."""
    out = binary_list.copy()
    for i in range(WORD_SIZE - 1, 0, -1):
        invert_bit_at(i, out)
    return out

def invert_bit(bit: int) -> int:
    """Инвертирует один переданный бит."""
    return 1 if bit == 0 else 0