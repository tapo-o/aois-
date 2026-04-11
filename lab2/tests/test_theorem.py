from src.advanced.theorem import (
    is_post_t0, is_post_t1, is_post_self_dual, 
    is_post_monotonic, is_post_linear, get_zhegalkin_coeffs
)
from src.core.analyzer import generate_truth_table

def test_classes_logic():
    _, t_const1 = generate_truth_table("a | !a")
    assert is_post_t1(t_const1) is True
    assert is_post_t0(t_const1) is False
    
    _, t_xor = generate_truth_table("!(a ~ b)")
    assert is_post_monotonic(t_xor) is False
    
    _, t_sd = generate_truth_table("!a")
    assert is_post_self_dual(t_sd) is True
    
def test_zhegalkin_and_linearity():
    # Линейная функция: отрицание эквивалентности (это и есть XOR)
    _, table = generate_truth_table("!(a ~ b)")
    f_vals = tuple(row[1] for row in table)
    coeffs = get_zhegalkin_coeffs(f_vals)
    assert is_post_linear(coeffs) is True
    
    # Нелинейная: a & b
    _, table_and = generate_truth_table("a & b")
    coeffs_and = get_zhegalkin_coeffs(tuple(r[1] for r in table_and))
    assert is_post_linear(coeffs_and) is False