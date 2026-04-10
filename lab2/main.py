from core.analyzer import (
    generate_truth_table, 
    get_boolean_derivative, 
    find_dummy_variables, 
    get_standard_forms, 
    get_numeric_forms, 
    get_index_form
)
from advanced.theorem import (
    is_post_t0, 
    is_post_t1, 
    is_post_self_dual, 
    is_post_monotonic, 
    build_zhegalkin_coeffs, 
    is_post_linear, 
    format_zhegalkin, 
    get_zhegalkin_coeffs
)
from minimizer.method import (
    get_prime_implicants_with_steps, 
    build_coverage_matrix, 
    build_karnaugh_map_string, 
    get_minimal_cover, 
    format_implicants
)
from parser.validator import validate_input

def run():
    print("="*60)
    print("АНАЛИЗАТОР БУЛЕВЫХ ФУНКЦИЙ (ЛАБОРАТОРНАЯ РАБОТА)")
    print("Поддерживаемые переменные: a, b, c, d, e")
    print("Операторы: & (И), | (ИЛИ), ! (НЕ), -> (Импл), ~ (Эквив)")
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
            
            idx_bin = "".join(map(str, f_values))
            print(f"\nИндексная форма (вектор): {idx_bin}")
            print(f"Десятичный индекс: {get_index_form(table)}")
            
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
            print(f"  - Сохранение нуля (T0):  {'+' if is_post_t0(table) else '-'}")
            print(f"  - Сохранение единицы (T1): {'+' if is_post_t1(table) else '-'}")
            print(f"  - Самодвойственность (S):  {'+' if is_post_self_dual(table) else '-'}")
            print(f"  - Монотонность (M):        {'+' if is_post_monotonic(table) else '-'}")
            print(f"  - Линейность (L):          {'+' if is_post_linear(coeffs) else '-'}")

            # 4. Булева дифференциация
            print("\n" + "="*40)
            print("БУЛЕВЫ ПРОИЗВОДНЫЕ")
            print("="*40)
            
            for i, var_name in enumerate(vars_tuple):
                deriv_table = get_boolean_derivative(table, i)
                deriv_vector = "".join([str(r[1]) for r in deriv_table])
                print(f"df/d{var_name}: {deriv_vector}")

            # 5. Минимизация
            print("\n" + "="*40)
            print("МИНИМИЗАЦИЯ ФУНКЦИИ")
            print("="*40)

            sdnf_rows = tuple(row[0] for row in table if row[1] == 1)
            sknf_rows = tuple(row[0] for row in table if row[1] == 0)

            # Расчет МДНФ
            print("\n>>> ЭТАПЫ ПОИСКА МДНФ (по единицам):")
            if not sdnf_rows:
                final_mdnf = "0"
                print("Функция тождественно ложна.")
            elif len(sdnf_rows) == 2**len(vars_tuple):
                final_mdnf = "1"
                print("Функция тождественно истинна.")
            else:
                prime_dnf, steps_dnf = get_prime_implicants_with_steps(sdnf_rows)
                for step in steps_dnf: print(step)
                print("\nМатрица покрытия для МДНФ:")
                print(build_coverage_matrix(prime_dnf, sdnf_rows))
                min_dnf = get_minimal_cover(prime_dnf, sdnf_rows)
                final_mdnf = format_implicants(min_dnf, vars_tuple, is_cnf=False)

            # Расчет МКНФ
            print("\n>>> ЭТАПЫ ПОИСКА МКНФ (по нулям):")
            if not sknf_rows:
                final_mknf = "1"
                print("Функция тождественно истинна.")
            elif len(sknf_rows) == 2**len(vars_tuple):
                final_mknf = "0"
                print("Функция тождественно ложна.")
            else:
                prime_cnf, steps_cnf = get_prime_implicants_with_steps(sknf_rows)
                for step in steps_cnf: print(step)
                print("\nМатрица покрытия для МКНФ:")
                print(build_coverage_matrix(prime_cnf, sknf_rows))
                min_cnf = get_minimal_cover(prime_cnf, sknf_rows)
                final_mknf = format_implicants(min_cnf, vars_tuple, is_cnf=True)

            print("\nИТОГОВЫЕ МИНИМАЛЬНЫЕ ФОРМЫ:")
            print(f"МДНФ: {final_mdnf}")
            print(f"МКНФ: {final_mknf}")

            # 6. Карта Карно
            print("\n>>> ТАБЛИЧНЫЙ МЕТОД (КАРТА КАРНО):")
            k_map = build_karnaugh_map_string(table, len(vars_tuple), vars_tuple)
            print(k_map)

            print("\n" + "="*60)

        except Exception as e:
            print(f"\n[!] ПРОИЗОШЛА ОШИБКА: {e}")
            # Для отладки раскомментируйте строку ниже:
            # import traceback; traceback.print_exc()

if __name__ == "__main__":
    run()