import sys

# Импорты для IEEE-754
from src.ieee import (
    float_to_ieee, ieee_to_float, 
    add_ieee, sub_ieee, multiply_ieee, divide_ieee
)
# Импорты для целых чисел (перевод и логика)
from src.transformInt import (
    dec_to_direct_bin, dec_to_reverse_bin, dec_to_twos_complement,
    direct_bin_to_dec, twos_complement_to_dec, fixedToDecimal
)
# Твои функции из src.binops
from src.binops import add_binary, subtract, multiply, divide
# Импорты для BCD
from src.bcd5421 import number_to_bcd_array, add_bcd_5421

def format_bits(bit_list: list[int]) -> str:
    return "".join(map(str, bit_list))

def get_float(prompt: str) -> float:
    while True:
        try: return float(input(prompt))
        except ValueError: print("Ошибка: введите число")

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
        if choice == "1": res_bin = add_ieee(b1, b2)
        elif choice == "2": res_bin = sub_ieee(b1, b2)
        elif choice == "3": res_bin = multiply_ieee(b1, b2)
        elif choice == "4": res_bin = divide_ieee(b1, b2)
        else: return

        print(f"\nРезультат (Float): {ieee_to_float(res_bin)}")
        print(f"Результат (Bits):  {format_bits(res_bin)}")
    except ZeroDivisionError:
        print("Ошибка: Деление на ноль!")

def handle_int_menu():
    print("\n--- ЦЕЛЫЕ ЧИСЛА ---")
    print("1. Посмотреть коды")
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

    if choice == "2": # Сложение (add_binary)
        b1, b2 = dec_to_twos_complement(n1), dec_to_twos_complement(n2)
        res = add_binary(b1, b2)
        print(f"\nРезультат (Dec):  {twos_complement_to_dec(res)}")
        print(f"Результат (Bits): {format_bits(res)}")

    elif choice == "3": # Вычитание (subtract)
        b1, b2 = dec_to_twos_complement(n1), dec_to_twos_complement(n2)
        res = subtract(b1, b2)
        print(f"\nРезультат (Dec):  {twos_complement_to_dec(res)}")
        print(f"Результат (Bits): {format_bits(res)}")

    elif choice == "4": # Умножение (multiply)
        b1, b2 = dec_to_direct_bin(n1), dec_to_direct_bin(n2)
        res = multiply(b1, b2)
        # Для корректного перевода в Dec используем прямой код
        print(f"\nРезультат (Dec):  {direct_bin_to_dec(res)}")
        print(f"Результат (Bits): {format_bits(res)}")

    elif choice == "5": # Деление (divide)
        b1, b2 = dec_to_direct_bin(n1), dec_to_direct_bin(n2)
        try:
            sign, integer, fraction = divide(b1, b2)
            # Используем твою функцию fixedToDecimal для красивого вывода
            res_decimal = fixedToDecimal(sign, integer, fraction)
            
            print(f"\nРезультат (Dec):    {res_decimal}")
            print(f"Знак (Bit):         {sign}")
            print(f"Целая часть (Bits):  {format_bits(integer)}")
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