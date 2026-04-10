import pytest
from parser.ast_builder import build_ast, evaluate_ast, get_variables_from_ast, build_ast_safe

def test_node_structure():
    node = build_ast("a & b")
    assert node.node_type == 'BINOP'
    assert node.value == '&'
    assert node.left.node_type == 'VAR'

def test_evaluation_all_ops():
    # Тестируем каждый оператор отдельно
    env = {'a': 1, 'b': 0}
    assert evaluate_ast(build_ast("a & b"), env) == 0
    assert evaluate_ast(build_ast("a | b"), env) == 1
    assert evaluate_ast(build_ast("!a"), env) == 0
    assert evaluate_ast(build_ast("a -> b"), env) == 0
    assert evaluate_ast(build_ast("a ~ b"), env) == 0
    assert evaluate_ast(build_ast("b -> a"), env) == 1

def test_complex_precedence():
    # !a | b & c должно быть (!a) | (b & c)
    node = build_ast("!a | b & c")
    env = {'a': 1, 'b': 1, 'c': 1}
    # !1 | 1&1 = 0 | 1 = 1
    assert evaluate_ast(node, env) == 1

def test_get_variables():
    node = build_ast("a & b | a & c")
    assert set(get_variables_from_ast(node)) == {'a', 'b', 'c'}

def test_ast_errors():
    with pytest.raises(ValueError):
        build_ast("a && b")
    node, err = build_ast_safe("((a)")
    assert "баланс скобок" in err