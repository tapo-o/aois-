from minimizer.method import (
    diff_by_one, get_prime_implicants_with_steps, 
    get_minimal_cover, format_implicants, build_karnaugh_map_string
)

def test_gluing():
    assert diff_by_one((1, 1), (1, 0)) == ((1, -1), True)
    assert diff_by_one((1, 1), (0, 0)) == (tuple(), False)

def test_quine_steps():
    terms = ((1, 1), (1, 0))
    primes, steps = get_prime_implicants_with_steps(terms)
    assert (1, -1) in primes
    assert "Стадия 1" in steps[0]

def test_coverage_and_format():
    primes = ((1, -1),)
    terms = ((1, 1), (1, 0))
    cover = get_minimal_cover(primes, terms)
    res = format_implicants(cover, ('a', 'b'))
    assert res == "a"

def test_empty_implicants():
    assert format_implicants([], ('a',), is_cnf=False) == "0"
    assert format_implicants([], ('a',), is_cnf=True) == "1"