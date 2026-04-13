from typing import Tuple, Set, List, Dict

# === ОБЩИЕ УТИЛИТЫ ===

def format_term(term: Tuple[int, ...]) -> str:
    return "".join(str(x) if x != -1 else "-" for x in term)

def covers(imp: Tuple[int, ...], term: Tuple[int, ...]) -> bool:
    return all(i == -1 or i == t for i, t in zip(imp, term))

def format_implicants(implicants, vars_tuple, is_cnf=False):
    if not implicants: return "1" if is_cnf else "0"
    formatted_list = []
    for imp in implicants:
        parts = []
        for i, val in enumerate(imp):
            if val == -1: continue
            if is_cnf:
                parts.append(f"{vars_tuple[i]}" if val == 0 else f"!{vars_tuple[i]}")
            else:
                parts.append(f"{vars_tuple[i]}" if val == 1 else f"!{vars_tuple[i]}")
        if len(parts) > 1:
            formatted_list.append(f"({' | '.join(parts)})" if is_cnf else f"({' & '.join(parts)})")
        elif len(parts) == 1:
            formatted_list.append(parts[0])
    return (" & " if is_cnf else " | ").join(formatted_list)

# === 1. ЛОГИКА МЕТОДА КВАЙНА (ПОСЛЕДОВАТЕЛЬНОЕ СКЛЕИВАНИЕ) ===

def diff_by_one(t1: Tuple[int, ...], t2: Tuple[int, ...]) -> Tuple[Tuple[int, ...], bool]:
    diffs = [i for i in range(len(t1)) if t1[i] != t2[i]]
    if len(diffs) == 1:
        res = list(t1)
        res[diffs[0]] = -1
        return tuple(res), True
    return tuple(), False

def quine_algorithm(terms: Tuple[Tuple[int, ...], ...], vars_tuple: Tuple[str, ...], is_cnf: bool) -> str:
    """Алгоритм Квайна: склеивание всех со всеми до упора."""
    print(f"\n--- ЭТАПЫ КВАЙНА ({'МКНФ' if is_cnf else 'МДНФ'}) ---")
    current = set(terms)
    prime_implicants = set()
    iteration = 1
    
    while current:
        print(f"Шаг {iteration} склеивания: {[format_term(t) for t in sorted(current)]}")
        next_gen = set()
        used = set()
        list_terms = sorted(list(current))
        for i in range(len(list_terms)):
            for j in range(i + 1, len(list_terms)):
                glued, ok = diff_by_one(list_terms[i], list_terms[j])
                if ok:
                    next_gen.add(glued)
                    used.add(list_terms[i])
                    used.add(list_terms[j])
        
        primes = current - used
        if primes:
            print(f"  Найдено простых импликант: {[format_term(p) for p in primes]}")
        prime_implicants.update(primes)
        current = next_gen
        iteration += 1

    print("\nТаблица покрытия:")
    print(build_coverage_matrix(sorted(prime_implicants), terms))

    uncovered = set(terms)
    final_set = []
    while uncovered:
        best = max(prime_implicants, key=lambda core: sum(1 for m in uncovered if covers(core, m)))
        final_set.append(best)
        uncovered = {m for m in uncovered if not covers(best, m)}
    
    return format_implicants(final_set, vars_tuple, is_cnf)

# === 2. ЛОГИКА МЕТОДА КВАЙНА-МАККЛАСКИ (ГРУППИРОВКА ПО ВЕСУ) ===

def qm_algorithm(terms: Tuple[Tuple[int, ...], ...], vars_tuple: Tuple[str, ...], is_cnf: bool) -> str:
    """Метод QM: группировка по количеству единиц и таблица покрытия."""
    print(f"\n--- ЭТАПЫ QM ({'МКНФ' if is_cnf else 'МДНФ'}) ---")
    groups: Dict[int, Set[Tuple[int, ...]]] = {}
    for t in terms:
        w = sum(1 for bit in t if bit == 1)
        groups.setdefault(w, set()).add(t)
    
    print("Начальная группировка по весу:")
    for w in sorted(groups.keys()):
        print(f"  Вес {w}: {[format_term(t) for t in groups[w]]}")
    
    prime_implicants = set()
    while groups:
        next_groups: Dict[int, Set[Tuple[int, ...]]] = {}
        used = set()
        keys = sorted(groups.keys())
        for i in range(len(keys) - 1):
            g1, g2 = groups[keys[i]], groups[keys[i+1]]
            for t1 in g1:
                for t2 in g2:
                    glued, ok = diff_by_one(t1, t2)
                    if ok:
                        w = sum(1 for bit in glued if bit == 1)
                        next_groups.setdefault(w, set()).add(glued)
                        used.add(t1)
                        used.add(t2)
        
        for k in groups:
            for t in groups[k]:
                if t not in used: prime_implicants.add(t)
        groups = next_groups

    print(f"Итоговые простые импликанты: {[format_term(p) for p in prime_implicants]}")

    cover = []
    uncovered = list(terms)
    # Поиск ядерных импликант
    for m in terms:
        hits = [p for p in prime_implicants if covers(p, m)]
        if len(hits) == 1 and hits[0] not in cover:
            print(f"  Выбрана ядерная импликанта {format_term(hits[0])} для покрытия {format_term(m)}")
            cover.append(hits[0])
    
    still_needed = [m for m in uncovered if not any(covers(p, m) for p in cover)]
    while still_needed:
        best = max(prime_implicants, key=lambda p: sum(1 for m in still_needed if covers(p, m)))
        cover.append(best)
        print(f"  Дополнительно выбран {format_term(best)}")
        still_needed = [m for m in still_needed if not covers(best, m)]

    return format_implicants(cover, vars_tuple, is_cnf)

# === 3. ЛОГИКА КАРТ КАРНО (ПОИСК МАКСИМАЛЬНЫХ ОБЛАСТЕЙ) ===

def get_all_possible_implicants(n: int) -> List[Tuple[int, ...]]:
    results = []
    def generate(current: List[int]):
        if len(current) == n:
            results.append(tuple(current))
            return
        for val in [0, 1, -1]:
            generate(current + [val])
    generate([])
    return results

def kmap_algorithm(terms: Tuple[Tuple[int, ...], ...], vars_tuple: Tuple[str, ...], is_cnf: bool) -> str:
    """Метод Карт Карно: поиск самого большого прямоугольника для каждой клетки."""
    print(f"\n--- ЭТАПЫ КАРНО ({'МКНФ' if is_cnf else 'МДНФ'}) ---")
    n = len(vars_tuple)
    target_cells = set(terms)
    all_possible = get_all_possible_implicants(n)
    
    valid_blocks = []
    for block in all_possible:
        block_cells = []
        def expand(curr, idx):
            if idx == n:
                block_cells.append(tuple(curr))
                return
            if block[idx] != -1:
                expand(curr + [block[idx]], idx + 1)
            else:
                expand(curr + [0], idx + 1)
                expand(curr + [1], idx + 1)
        expand([], 0)
        
        if all(c in target_cells for c in block_cells):
            valid_blocks.append((block, len(block_cells)))

    valid_blocks.sort(key=lambda x: x[1], reverse=True)
    
    final_cover = []
    remaining = set(terms)
    print("Поиск максимальных областей:")
    for block, size in valid_blocks:
        covered_by_this = [c for c in remaining if covers(block, c)]
        if covered_by_this:
            print(f"  Выбран блок {format_term(block)} размера {size}, покрывает: {[format_term(c) for c in covered_by_this]}")
            final_cover.append(block)
            for c in covered_by_this:
                remaining.remove(c)
        if not remaining: break
            
    return format_implicants(final_cover, vars_tuple, is_cnf)

# === ФУНКЦИИ ЛОГИРОВАНИЯ И ВИЗУАЛИЗАЦИИ ===

def build_coverage_matrix(implicants, minterms) -> str:
    header = "Импл. | " + " | ".join(f"{format_term(m)}" for m in minterms)
    rows = [header, "-" * len(header)]
    for imp in implicants:
        row = f"{format_term(imp):<5} | " + " | ".join("  X  " if covers(imp, m) else "     " for m in minterms)
        rows.append(row)
    return "\n".join(rows)

def build_karnaugh_map_string(table, vars_count, vars_tuple) -> str:
    table_dict = {"".join(map(str, row[0])): row[1] for row in table}
    if vars_count == 1:
        cols, rows = ("0", "1"), ("",)
        row_vars, col_vars = "", vars_tuple[0]
    elif vars_count == 2:
        cols, rows = ("0", "1"), ("0", "1")
        row_vars, col_vars = vars_tuple[0], vars_tuple[1]
    elif vars_count == 3:
        cols, rows = ("00", "01", "11", "10"), ("0", "1")
        row_vars, col_vars = vars_tuple[0], "".join(vars_tuple[1:])
    elif vars_count == 4:
        cols, rows = ("00", "01", "11", "10"), ("00", "01", "11", "10")
        row_vars, col_vars = "".join(vars_tuple[:2]), "".join(vars_tuple[2:])
    elif vars_count == 5:
        cols = ("000", "001", "011", "010", "110", "111", "101", "100")
        rows = ("00", "01", "11", "10")
        row_vars, col_vars = "".join(vars_tuple[:2]), "".join(vars_tuple[2:])
    else:
        return "Карта слишком велика для вывода в консоль (максимум 5 переменных)."

    header_corner = f"{row_vars}\\{col_vars}" if row_vars else f"\\{col_vars}"
    pad = max(len(header_corner), max(len(r) for r in rows) if rows[0] else 0)
    res = []
    header_line = f"{header_corner:<{pad}} | " + " | ".join(f"{c:^{len(c)}}" for c in cols)
    res.append(header_line)
    res.append("-" * len(header_line))
    for r in rows:
        line = [f"{r:<{pad}}"]
        for c in cols:
            key = r + c
            val = str(table_dict.get(key, "?"))
            line.append(f"{val:^{len(c)}}")
        res.append(" | ".join(line))
    return "\n".join(res)