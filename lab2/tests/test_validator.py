import pytest
from src.parser.validator import validate_input

def test_valid_inputs():
    assert validate_input("a & b") == "a&b"
    assert validate_input("!a -> (b ~ c)") == "!a->(b~c)"

def test_invalid_chars():
    with pytest.raises(ValueError, match="запрещенные символы"):
        validate_input("a + b")
    with pytest.raises(ValueError, match="запрещенные символы"):
        validate_input("a @ b")

def test_empty_and_spaces():
    with pytest.raises(ValueError, match="пуста"):
        validate_input("   ")
    with pytest.raises(ValueError, match="пустые скобки"):
        validate_input("a & ()")

def test_implication_safety():
    with pytest.raises(ValueError, match="составе импликации"):
        validate_input("a - b")