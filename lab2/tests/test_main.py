import pytest
from unittest.mock import patch
from main import run

@patch('builtins.input')
def test_full_flow(mock_input, capsys):
    # Симулируем ввод нескольких выражений и выход
    mock_input.side_effect = [
        "a & b", 
        "a | !a", 
        "q"
    ]
    run()
    captured = capsys.readouterr()
    assert "ТАБЛИЦА ИСТИННОСТИ" in captured.out
    assert "Полином Жегалкина" in captured.out
    assert "МДНФ" in captured.out

@patch('builtins.input')
def test_main_error_resilience(mock_input, capsys):
    # Проверка, что программа не вылетает при ошибке ввода
    mock_input.side_effect = ["wrong expression!!!", "q"]
    run()
    captured = capsys.readouterr()
    assert "ПРОИЗОШЛА ОШИБКА" in captured.out