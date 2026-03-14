"""Константы для работы с бинарной арифметикой и IEEE-754."""

WORD_SIZE = 32
ONE = [0] * (WORD_SIZE - 1) + [1]
MONE = [1] * (WORD_SIZE - 1) + [0]
FRACDIGITS = 5
BIAS = 127