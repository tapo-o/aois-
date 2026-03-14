import sys
from src.ieee import (
    float_to_ieee, ieee_to_float, 
    add_ieee, sub_ieee, multiply_ieee, divide_ieee
)
from src.transformInt import (
    dec_to_direct_bin, dec_to_reverse_bin, dec_to_twos_complement
)
from src.bcd5421 import number_to_bcd_array, add_bcd_5421

def format_bits(bit_list: list[int]) -> str:
    return "".join(map(str, bit_list))

def get_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число (например, 13.5 или -0.1)")

def get_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число")

def show_menu():
    print("\n" + "="*40)
    print("   ЭМУЛЯТОР БИНАРНОЙ АРИФМЕТИКИ")
    print("="*40)
    print("1. IEEE-754 (Плавающая точка)")
    print("2. Целые числа (Прямой/Обратный/Доп. коды)")
    print("3. BCD 5421 (Двоично-десятичный код)")
    print("0. Выход")
    print("-"*40)

def handle_ieee_menu():
    print("\n--- ОПЕРАЦИИ IEEE-754 ---")
    print("1. Сложить (+)")
    print("2. Вычесть (-)")
    print("3. Умножить (*)")
    print("4. Разделить (/)")
    print("5. Число -> IEEE-754 (Кодирование)")
    
    choice = input("\nВыберите операцию: ")
    
    if choice == "5":
        val = get_float("Введите число: ")
        res = float_to_ieee(val)
        print(f"Результат: {format_bits(res)}")
        return

    v1 = get_float("Введите первое число: ")
    v2 = get_float("Введите второе число: ")
    
    bin1, bin2 = float_to_ieee(v1), float_to_ieee(v2)
    
    try:
        if choice == "1":
            res_bin = add_ieee(bin1, bin2)
        elif choice == "2":
            res_bin = sub_ieee(bin1, bin2)
        elif choice == "3":
            res_bin = multiply_ieee(bin1, bin2)
        elif choice == "4":
            res_bin = divide_ieee(bin1, bin2)
        else:
            print("Неверный выбор.")
            return

        print(f"\nРезультат (Float): {ieee_to_float(res_bin)}")
        print(f"Результат (Bits):  {format_bits(res_bin)}")
    except ZeroDivisionError:
        print("Ошибка: Деление на ноль!")

def handle_int_menu():
    print("\n--- ЦЕЛЫЕ ЧИСЛА ---")
    num = get_int("Введите целое число: ")
    
    print(f"Прямой код:  {format_bits(dec_to_direct_bin(num))}")
    print(f"Обратный код: {format_bits(dec_to_reverse_bin(num))}")
    print(f"Доп. код:     {format_bits(dec_to_twos_complement(num))}")

def handle_bcd_menu():
    print("\n--- BCD 5421 ---")
    print("1. Закодировать число")
    print("2. Сложить два числа")
    
    choice = input("\nВыберите операцию: ")
    
    if choice == "1":
        val = get_int("Введите число: ")
        res = number_to_bcd_array(val)
        print(f"Результат: {' '.join(format_bits(b) for b in res)}")
    elif choice == "2":
        v1 = get_int("Введите первое число: ")
        v2 = get_int("Введите второе число: ")
        res = add_bcd_5421(number_to_bcd_array(v1), number_to_bcd_array(v2))
        print(f"Результат сложения: {' '.join(format_bits(b) for b in res)}")

def main():
    while True:
        show_menu()
        choice = input("Введите номер раздела: ")
        
        if choice == "1":
            handle_ieee_menu()
        elif choice == "2":
            handle_int_menu()
        elif choice == "3":
            handle_bcd_menu()
        elif choice == "0":
            break
        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()