from src.minimizer.method import (
    diff_by_one, 
    format_implicants,
    covers
)

def test_gluing():
    assert diff_by_one((1, 1), (1, 0)) == ((1, -1), True)
    assert diff_by_one((1, 1), (0, 0)) == (tuple(), False)
    assert diff_by_one((1, -1, 0), (1, -1, 1)) == ((1, -1, -1), True)

def test_covers():
    imp = (1, -1, 0)
    assert covers(imp, (1, 0, 0)) is True
    assert covers(imp, (1, 1, 0)) is True
    assert covers(imp, (0, 0, 0)) is False 
    assert covers(imp, (1, 0, 1)) is False 

def test_empty_and_full_cases():
    assert format_implicants([], ('a',), is_cnf=False) == "0"
    assert format_implicants([], ('a',), is_cnf=True) == "1"