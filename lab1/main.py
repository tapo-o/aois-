import sys

# Импорты для IEEE-754
from src.ieee import (
    float_to_ieee, ieee_to_float, 
    add_ieee, sub_ieee, multiply_ieee, divide_ieee
)
# Импорты для целых чисел (перевод)
from src.transformInt import (
    dec_to_direct_bin, dec_to_reverse_bin, dec_to_twos_complement,
    direct_bin_to_dec, twos_complement_to_dec
)
# Импорты для целых чисел (арифметика)
from src.binops import add_binary, subtract, multiply, divide
# Импорты для BCD
from src.bcd5421 import number_to_bcd_array, add_bcd_5421

def format_bits(bit_list: list[int]) -> str:
    return "".join(map(str, bit_list))

def get_float(prompt: str) -> float:
    while True:
        try: return float(input(prompt))
        except ValueError: print("Ошибка: введите число (13.5)")

def get_int(prompt: str) -> int:
    while True:
        try: return int(input(prompt))
        except ValueError: print("Ошибка: введите целое число")

def show_menu():
    print("\n" + "="*40)
    print("   ЭМУЛЯТОР БИНАРНОЙ АРИФМЕТИКИ")
    print("="*40)
    print("1. IEEE-754 (Плавающая точка)")
    print("2. Целые числа (Коды и Арифметика)")
    print("3. BCD 5421 (Двоично-десятичный код)")
    print("0. Выход")
    print("-"*40)

def handle_ieee_menu():
    print("\n--- ОПЕРАЦИИ IEEE-754 ---")
    print("1. Сложить | 2. Вычесть | 3. Умножить | 4. Разделить | 5. Кодировать")
    choice = input("\nВыберите операцию: ")
    
    if choice == "5":
        val = get_float("Введите число: ")
        print(f"Результат: {format_bits(float_to_ieee(val))}")
        return

    v1, v2 = get_float("Введите 1-е число: "), get_float("Введите 2-е число: ")
    b1, b2 = float_to_ieee(v1), float_to_ieee(v2)
    
    try:
        ops = {"1": add_ieee, "2": sub_ieee, "3": multiply_ieee, "4": divide_ieee}
        if choice in ops:
            res_bin = ops[choice](b1, b2)
            print(f"\nРезультат (Float): {ieee_to_float(res_bin)}")
            print(f"Результат (Bits):  {format_bits(res_bin)}")
    except ZeroDivisionError:
        print("Ошибка: Деление на ноль!")

def handle_int_menu():
    print("\n--- ЦЕЛЫЕ ЧИСЛА ---")
    print("1. Посмотреть коды числа (прямой/обратный/доп)")
    print("2. Сложение (+)")
    print("3. Вычитание (-)")
    print("4. Умножение (*)")
    print("5. Деление (/)")
    
    choice = input("\nВыберите операцию: ")
    
    if choice == "1":
        num = get_int("Введите число: ")
        print(f"Прямой:  {format_bits(dec_to_direct_bin(num))}")
        print(f"Обратный: {format_bits(dec_to_reverse_bin(num))}")
        print(f"Доп. код: {format_bits(dec_to_twos_complement(num))}")
        return

    n1 = get_int("Введите 1-е число: ")
    n2 = get_int("Введите 2-е число: ")

    if choice == "2": # Сложение
        b1, b2 = dec_to_twos_complement(n1), dec_to_twos_complement(n2)
        res = add_binary(b1, b2)
        print(f"Результат (Dec):  {twos_complement_to_dec(res)}")
        print(f"Результат (Bits): {format_bits(res)}")

    elif choice == "3": # Вычитание
        b1, b2 = dec_to_twos_complement(n1), dec_to_twos_complement(n2)
        res = subtract(b1, b2)
        print(f"Результат (Dec):  {twos_complement_to_dec(res)}")
        print(f"Результат (Bits): {format_bits(res)}")

    elif choice == "4": # Умножение
        b1, b2 = dec_to_direct_bin(n1), dec_to_direct_bin(n2)
        res = multiply(b1, b2)
        print(f"Результат (Dec):  {direct_bin_to_dec(res)}")
        print(f"Результат (Bits): {format_bits(res)}")

    elif choice == "5": # Деление
        b1, b2 = dec_to_direct_bin(n1), dec_to_direct_bin(n2)
        try:
            sign, integer, fraction = divide(b1, b2)
            # Для простоты вывода покажем целую часть
            res_dec = direct_bin_to_dec([sign] + integer[1:])
            print(f"Целая часть (Dec): {res_dec}")
            print(f"Целая часть (Bits): {format_bits(integer)}")
            print(f"Дробная часть (Bits): {format_bits(fraction)}")
        except ValueError as e:
            print(f"Ошибка: {e}")

def handle_bcd_menu():
    print("\n--- BCD 5421 ---")
    print("1. Закодировать | 2. Сложить")
    choice = input("\nВыберите операцию: ")
    
    if choice == "1":
        val = get_int("Введите число: ")
        res = number_to_bcd_array(val)
        print(f"Результат: {' '.join(format_bits(b) for b in res)}")
    elif choice == "2":
        v1, v2 = get_int("Введите 1-е число: "), get_int("Введите 2-е число: ")
        res = add_bcd_5421(number_to_bcd_array(v1), number_to_bcd_array(v2))
        print(f"Результат BCD: {' '.join(format_bits(b) for b in res)}")

def main():
    while True:
        show_menu()
        choice = input("Введите номер раздела: ")
        if choice == "1": handle_ieee_menu()
        elif choice == "2": handle_int_menu()
        elif choice == "3": handle_bcd_menu()
        elif choice == "0": break
        else: print("Неверный ввод.")

if __name__ == "__main__":
    main()