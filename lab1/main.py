import sys

# Импорты для IEEE-754
from src.ieee import (
    float_to_ieee, ieee_to_float, 
    add_ieee, sub_ieee, multiply_ieee, divide_ieee
)
# Импорты для перевода целых чисел
from src.transformInt import (
    dec_to_direct_bin, dec_to_reverse_bin, dec_to_twos_complement,
    direct_bin_to_dec, reverse_bin_to_dec, twos_complement_to_dec, fixedToDecimal
)
# Импорты бинарных операций
from src.binops import add_binary, subtract, multiply, divide
# Импорты BCD
from src.bcd5421 import number_to_bcd_array, add_bcd_5421

def format_bits(bit_list: list[int]) -> str:
    """Преобразует список бит в строку для вывода."""
    return "".join(map(str, bit_list))

def print_all_int_codes(label: str, num: int):
    """Выводит число во всех трех представлениях."""
    direct = dec_to_direct_bin(num)
    reverse = dec_to_reverse_bin(num)
    twos = dec_to_twos_complement(num)
    
    print(f"--- {label} ({num}) ---")
    print(f"  Прямой код:  {format_bits(direct)}")
    print(f"  Обратный:    {format_bits(reverse)}")
    print(f"  Доп. код:    {format_bits(twos)}")

def print_result_in_all_codes(res_bits: list[int], mode: str):
    """
    Выводит результат операции во всех кодах.
    mode: 'dop' если результат в дополнительном коде, 'direct' если в прямом.
    """
    # Сначала узнаем десятичное значение, чтобы построить остальные коды
    if mode == 'dop':
        val = twos_complement_to_dec(res_bits)
    else:
        val = direct_bin_to_dec(res_bits)
        
    print(f"\nИТОГОВЫЙ РЕЗУЛЬТАТ:")
    print_all_int_codes("В десятичном виде", val)

def get_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число")

def get_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число (например, 13.5)")

def handle_int_menu():
    print("\n--- ЦЕЛЫЕ ЧИСЛА ---")
    print("1. Посмотреть ВСЕ КОДЫ числа")
    print("2. Сложение (+)")
    print("3. Вычитание (-)")
    print("4. Умножение (*)")
    print("5. Деление (/)")
    
    choice = input("\nВыберите номер: ")
    
    if choice == "1":
        num = get_int("Введите целое число: ")
        print()
        print_all_int_codes("Представление числа", num)
        return

    n1 = get_int("Введите 1-е число: ")
    n2 = get_int("Введите 2-е число: ")

    print("\nВходные данные:")
    print_all_int_codes("Число 1", n1)
    print_all_int_codes("Число 2", n2)
    print("-" * 45)

    if choice == "2":
        # Сложение выполняется в доп. коде
        res = add_binary(dec_to_twos_complement(n1), dec_to_twos_complement(n2))
        print_result_in_all_codes(res, 'dop')

    elif choice == "3":
        # Вычитание выполняется в доп. коде
        res = subtract(dec_to_twos_complement(n1), dec_to_twos_complement(n2))
        print_result_in_all_codes(res, 'dop')

    elif choice == "4":
        # Умножение обычно возвращает прямой код (знак + модуль)
        res = multiply(dec_to_direct_bin(n1), dec_to_direct_bin(n2))
        print_result_in_all_codes(res, 'direct')

    elif choice == "5":
        try:
            # Деление возвращает компоненты числа с фиксированной точкой
            sign, integer, fraction = divide(dec_to_direct_bin(n1), dec_to_direct_bin(n2))
            res_dec = fixedToDecimal(sign, integer, fraction)
            print(f"\nИТОГОВЫЙ РЕЗУЛЬТАТ (Фикс. точка):")
            print(f"  Десятичное:    {res_dec}")
            print(f"  Знак (бит):    {sign}")
            print(f"  Целая часть:   {format_bits(integer)}")
            print(f"  Дробная часть: {format_bits(fraction)}")
        except ValueError as e:
            print(f"Ошибка: {e}")

def handle_ieee_menu():
    print("\n--- IEEE-754 ---")
    print("1. Сложение | 2. Вычитание | 3. Умножение | 4. Деление | 5. Код числа")
    op = input("\nВыберите: ")
    
    if op == "5":
        val = get_float("Введите число: ")
        print(f"IEEE-754: {format_bits(float_to_ieee(val))}")
        return

    v1, v2 = get_float("1-е число: "), get_float("2-е число: ")
    b1, b2 = float_to_ieee(v1), float_to_ieee(v2)
    
    try:
        if op == "1": res = add_ieee(b1, b2)
        elif op == "2": res = sub_ieee(b1, b2)
        elif op == "3": res = multiply_ieee(b1, b2)
        elif op == "4": res = divide_ieee(b1, b2)
        else: return
        print(f"\nРезультат (Dec): {ieee_to_float(res)}")
        print(f"Биты: {format_bits(res)}")
    except ZeroDivisionError:
        print("Ошибка: Деление на ноль!")

def handle_bcd_menu():
    print("\n--- BCD 5421 ---")
    print("1. Кодировать | 2. Сложить")
    op = input("\nВыберите: ")
    if op == "1":
        val = get_int("Число: ")
        res = number_to_bcd_array(val)
        print(f"BCD: {' '.join(format_bits(b) for b in res)}")
    elif op == "2":
        n1, n2 = get_int("1-е: "), get_int("2-е: ")
        res = add_bcd_5421(number_to_bcd_array(n1), number_to_bcd_array(n2))
        print(f"Сумма BCD: {' '.join(format_bits(b) for b in res)}")

def main():
    while True:
        print("\n" + "="*45)
        print("      ЭМУЛЯТОР БИНАРНОЙ АРИФМЕТИКИ")
        print("="*45)
        print("1. IEEE-754 (Плавающая точка)")
        print("2. Целые числа (Все коды и Арифметика)")
        print("3. BCD 5421 (Двоично-десятичный код)")
        print("0. Выход")
        
        choice = input("\nРаздел: ")
        if choice == "1": handle_ieee_menu()
        elif choice == "2": handle_int_menu()
        elif choice == "3": handle_bcd_menu()
        elif choice == "0": break

if __name__ == "__main__":
    main()