from core.analyzer import (
    generate_truth_table, find_dummy_variables, 
    get_standard_forms, get_numeric_forms, get_index_form
)

def test_truth_table_generation():
    vars_tuple, table = generate_truth_table("a & b")
    assert vars_tuple == ('a', 'b')
    assert len(table) == 4
    assert table[3][1] == 1 # 1 & 1 = 1

def test_dummy_variables():
    # В функции 'a | b & !b' переменная 'b' не влияет на результат
    _, table = generate_truth_table("a | b & !b")
    dummies = find_dummy_variables(table, 2)
    assert dummies == (1,)

def test_forms_output():
    _, table = generate_truth_table("a & b")
    sdnf, sknf = get_standard_forms(table, ('a', 'b'))
    assert "a & b" in sdnf
    
    sdnf_n, sknf_n = get_numeric_forms(table)
    assert sdnf_n == (3,)
    assert sknf_n == (0, 1, 2)
    
    # Исправленное ожидание: 1 (так как 1*2^0 = 1)
    assert get_index_form(table) == 1