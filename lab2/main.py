from src.core.analyzer import (
    generate_truth_table, 
    get_boolean_derivative, 
    find_dummy_variables, 
    get_standard_forms, 
    get_numeric_forms, 
    get_index_form,
    get_multiple_derivative,
    get_combinations
)
from src.advanced.theorem import (
    is_post_t0, 
    is_post_t1, 
    is_post_self_dual, 
    is_post_monotonic, 
    build_zhegalkin_coeffs, 
    is_post_linear, 
    format_zhegalkin, 
    get_zhegalkin_coeffs
)
# Импортируем обновленные функции из нового method.py
from src.minimizer.method import (
    quine_algorithm,
    qm_algorithm,
    kmap_algorithm,
    build_karnaugh_map_string,
    build_coverage_matrix
)
from src.parser.validator import validate_input

def run():
    print("="*60)
    print("УНИВЕРСАЛЬНЫЙ АНАЛИЗАТОР И МИНИМИЗАТОР БУЛЕВЫХ ФУНКЦИЙ")
    print("="*60)

    while True:
        try:
            expr_input = input("\nВведите выражение (или 'q' для выхода): ").strip()
            if expr_input.lower() in ('exit', 'quit', 'q'):
                print("Завершение работы.")
                break
                
            # 1. Валидация и парсинг
            expr = validate_input(expr_input)
            vars_tuple, table = generate_truth_table(expr)
            f_values = tuple(row[1] for row in table)
            
            # 2. Таблица истинности и формы
            print(f"\n[ РЕЗУЛЬТАТЫ АНАЛИЗА ДЛЯ: {expr_input} ]")
            print("-" * 40)
            print("ТАБЛИЦА ИСТИННОСТИ:")
            header = " | ".join(vars_tuple) + " || F"
            print(header)
            print("-" * len(header))
            for row in table:
                vals = " | ".join(map(str, row[0]))
                print(f"{vals} || {row[1]}")
            
            print(f"\nДесятичный индекс: {get_index_form(table)}")
            
            sdnf_nums, sknf_nums = get_numeric_forms(table)
            print(f"Числовая форма СДНФ: ∑({', '.join(map(str, sdnf_nums))})")
            print(f"Числовая форма СКНФ: ∏({', '.join(map(str, sknf_nums))})")
            
            sdnf_str, sknf_str = get_standard_forms(table, vars_tuple)
            print(f"\nСДНФ: {sdnf_str}")
            print(f"СКНФ: {sknf_str}")

            # 3. Полином Жегалкина и Классы Поста
            print("\n" + "="*40)
            print("МАТЕМАТИЧЕСКИЙ АНАЛИЗ")
            print("="*40)
            
            coeffs = get_zhegalkin_coeffs(f_values)
            zhegalkin_res = format_zhegalkin(coeffs, vars_tuple)
            print(f"Полином Жегалкина: {zhegalkin_res}")
            
            dummies = find_dummy_variables(table, len(vars_tuple))
            print(f"Фиктивные переменные: {', '.join([vars_tuple[i] for i in dummies]) if dummies else 'Нет'}")

            print("\nПРОВЕРКА КЛАССОВ ПОСТА:")
            print(f"  - T0: {'+' if is_post_t0(table) else '-'}")
            print(f"  - T1: {'+' if is_post_t1(table) else '-'}")
            print(f"  - S:  {'+' if is_post_self_dual(table) else '-'}")
            print(f"  - M:  {'+' if is_post_monotonic(table) else '-'}")
            print(f"  - L:  {'+' if is_post_linear(coeffs) else '-'}")

            # 4. Булева дифференциация
            print("\n" + "="*40)
            print("БУЛЕВЫ ПРОИЗВОДНЫЕ")
            print("="*40)
            indices = tuple(range(len(vars_tuple)))
            for r in range(1, len(vars_tuple) + 1):
                combos = get_combinations(indices, r)
                for combo in combos:
                    deriv_table = get_multiple_derivative(table, combo)
                    deriv_vector = "".join([str(row[1]) for row in deriv_table])
                    var_names = "".join([vars_tuple[i] for i in combo])
                    print(f"d f / d {var_names}: {deriv_vector}")

            # Подготовка данных для минимизации
            ones = tuple(row[0] for row in table if row[1] == 1)
            zeros = tuple(row[0] for row in table if row[1] == 0)

            # 7. Визуализация
            
            
            # 5. Минимизация МДНФ
            print("\n" + "="*40)
            print("МИНИМИЗАЦИЯ ФУНКЦИИ (МДНФ)")
            print("="*40)

            if not ones:
                print("Функция ≡ 0")
            elif len(ones) == 2**len(vars_tuple):
                print("Функция ≡ 1")
            else:
                # В новых алгоритмах логика поиска импликант встроена внутрь
                print(f"1. Метод Квайна (Склеивание):  {quine_algorithm(ones, vars_tuple, False)}")
                print(f"2. Метод QM (Группировка):     {qm_algorithm(ones, vars_tuple, False)}")
                print("\n" + "="*40)
                print("ВИЗУАЛИЗАЦИЯ (КАРТА КАРНО)")
                print("="*40)
                print(build_karnaugh_map_string(table, len(vars_tuple), vars_tuple))
                print(f"3. Метод Карно (Геометрия):    {kmap_algorithm(ones, vars_tuple, False)}")

            # 6. Минимизация МКНФ
            print("\n" + "="*40)
            print("МИНИМИЗАЦИЯ ФУНКЦИИ (МКНФ)")
            print("="*40)

            if not zeros:
                print("Функция ≡ 1")
            elif len(zeros) == 2**len(vars_tuple):
                print("Функция ≡ 0")
            else:
                print(f"1. Метод Квайна (Склеивание):  {quine_algorithm(zeros, vars_tuple, True)}")
                print(f"2. Метод QM (Группировка):     {qm_algorithm(zeros, vars_tuple, True)}")
                print("\n" + "="*40)
                print("ВИЗУАЛИЗАЦИЯ (КАРТА КАРНО)")
                print("="*40)
                print(build_karnaugh_map_string(table, len(vars_tuple), vars_tuple))
                print(f"3. Метод Карно (Геометрия):    {kmap_algorithm(zeros, vars_tuple, True)}")
            print("\n" + "="*60)

        except Exception as e:
            print(f"\n[!] ПРОИЗОШЛА ОШИБКА: {e}")

if __name__ == "__main__":
    run()