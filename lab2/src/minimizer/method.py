from typing import Tuple, Set, List

# === Расчетный метод (Куайн) ===
def diff_by_one(term1: Tuple[int, ...], term2: Tuple[int, ...]) -> Tuple[Tuple[int, ...], bool]:
    diff_count = sum(1 for a, b in zip(term1, term2) if a != b)
    if diff_count == 1:
        # Сохраняем значения, которые совпали, и ставим -1 (прочерк) там, где различие
        return tuple(a if a == b else -1 for a, b in zip(term1, term2)), True
    return tuple(), False

def format_term(term: Tuple[int, ...]) -> str:
    return "".join(str(x) if x != -1 else "-" for x in term)

def get_prime_implicants_with_steps(terms: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[Tuple[int, ...], ...], List[str]]:
    steps_log = []
    current_terms = set(terms)
    all_prime_implicants = set()
    stage = 1

    while current_terms:
        next_terms = set()
        used_in_gluing = set()
        stage_log = [f"Стадия {stage}:"]
        
        term_list = sorted(list(current_terms))
        for i in range(len(term_list)):
            for j in range(i + 1, len(term_list)):
                glued, success = diff_by_one(term_list[i], term_list[j])
                if success:
                    next_terms.add(glued)
                    used_in_gluing.add(term_list[i])
                    used_in_gluing.add(term_list[j])
                    stage_log.append(f"  {format_term(term_list[i])} + {format_term(term_list[j])} -> {format_term(glued)}")
        
        unmerged = current_terms - used_in_gluing
        all_prime_implicants.update(unmerged)
        
        if not next_terms:
            if stage == 1 and not next_terms:
                steps_log.append("  Склеивание невозможно.")
            else:
                steps_log.extend(stage_log)
                steps_log.append("  Процесс склеивания завершен.")
            break
            
        steps_log.extend(stage_log)
        steps_log.append("")
        current_terms = next_terms
        stage += 1
        
    return tuple(sorted(list(all_prime_implicants))), steps_log

# === Минимальное покрытие ===
def covers(imp: Tuple[int, ...], term: Tuple[int, ...]) -> bool:
    return all(i == -1 or i == t for i, t in zip(imp, term))

def get_minimal_cover(prime_implicants: Tuple[Tuple[int, ...], ...], terms: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[int, ...], ...]:
    uncovered = set(terms)
    cover = []
    
    for m in terms:
        covering = [imp for imp in prime_implicants if covers(imp, m)]
        if len(covering) == 1 and covering[0] not in cover:
            cover.append(covering[0])
                
    for imp in cover:
        uncovered -= {m for m in uncovered if covers(imp, m)}
        
    remaining_imps = list(set(prime_implicants) - set(cover))
    while uncovered:
        if not remaining_imps: break
        best_imp = max(remaining_imps, key=lambda imp: sum(1 for m in uncovered if covers(imp, m)))
        cover.append(best_imp)
        remaining_imps.remove(best_imp)
        uncovered -= {m for m in uncovered if covers(best_imp, m)}
        
    return tuple(cover)

def format_implicants(implicants, vars_tuple, is_cnf=False):
    """Форматирует результат в МДНФ или МКНФ (учитывая инверсию для МКНФ)."""
    if not implicants: return "1" if is_cnf else "0"
    
    formatted_list = []
    for imp in implicants:
        parts = []
        for i, val in enumerate(imp):
            if val == -1: continue
            if is_cnf:
                # В МКНФ: 0 -> x, 1 -> !x
                parts.append(f"{vars_tuple[i]}" if val == 0 else f"!{vars_tuple[i]}")
            else:
                # В МДНФ: 1 -> x, 0 -> !x
                parts.append(f"{vars_tuple[i]}" if val == 1 else f"!{vars_tuple[i]}")
        
        if len(parts) > 1:
            formatted_list.append(f"({' | '.join(parts)})" if is_cnf else f"({' & '.join(parts)})")
        elif len(parts) == 1:
            formatted_list.append(parts[0])
            
    separator = " & " if is_cnf else " | "
    return separator.join(formatted_list)

# === Матрица покрытия ===
def build_coverage_matrix(implicants: Tuple[Tuple[int, ...], ...], minterms: Tuple[Tuple[int, ...], ...]) -> str:
    header = "Импликанта | " + " | ".join(f"{str(i+1):^3}" for i in range(len(minterms)))
    rows = []
    for imp in implicants:
        imp_str = format_term(imp)
        row_marks = [" X " if covers(imp, m) else "   " for m in minterms]
        rows.append(f"{imp_str:<10} | " + " | ".join(row_marks))
    return "\n".join([header, "-" * len(header)] + rows)

# === Карта Карно (2-5 переменных) ===
def build_karnaugh_map_string(table, vars_count, vars_tuple) -> str:
    table_dict = {"".join(map(str, row[0])): row[1] for row in table}
    
    def render_4x4(fixed_prefix=""):
        # Отрисовка стандартного блока 4x4 (или меньше)
        if vars_count - len(fixed_prefix) == 2:
            cols, rows = ("0", "1"), ("0", "1")
            v_row, v_col = vars_tuple[len(fixed_prefix)], vars_tuple[len(fixed_prefix)+1]
        elif vars_count - len(fixed_prefix) == 3:
            cols, rows = ("00", "01", "11", "10"), ("0", "1")
            v_row, v_col = vars_tuple[len(fixed_prefix)], vars_tuple[len(fixed_prefix)+1:]
        else: # 4 переменные в блоке
            cols, rows = ("00", "01", "11", "10"), ("00", "01", "11", "10")
            v_row, v_col = vars_tuple[len(fixed_prefix):len(fixed_prefix)+2], vars_tuple[len(fixed_prefix)+2:]
        
        v_col_str = "".join(v_col)
        v_row_str = "".join(v_row)
        header = f" {v_row_str}\\{v_col_str} | " + " | ".join(cols)
        lines = [header, "-" * len(header)]
        
        for r_val in rows:
            row_cells = []
            for c_val in cols:
                key = fixed_prefix + r_val + c_val
                row_cells.append(str(table_dict.get(key, '?')))
            lines.append(f"{r_val:>{len(v_row_str)}} | " + " | ".join(f"{c:^{len(cols[0])}}" for c in row_cells))
        return "\n".join(lines)

    if vars_count <= 4:
        return render_4x4()
    elif vars_count == 5:
        # Для 5 переменных рисуем две карты: для первого бита = 0 и для бита = 1
        map0 = render_4x4(fixed_prefix="0")
        map1 = render_4x4(fixed_prefix="1")
        return f"ПЛОСКОСТЬ {vars_tuple[0]}=0:\n{map0}\n\nПЛОСКОСТЬ {vars_tuple[0]}=1:\n{map1}"
    return "Карта Карно не поддерживается для данного кол-ва переменных."