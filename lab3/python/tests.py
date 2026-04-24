import pytest
from unittest.mock import patch

from Implicant import Implicant
from Equation import Equation
import qm
import circuits
import main
from constants import OFFSET_N


# ==========================================
# Тесты для Implicant.py
# ==========================================
class TestImplicant:
    def test_is_equal(self):
        imp1 = Implicant(value=2, mask=1)
        imp2 = Implicant(value=2, mask=1)
        imp3 = Implicant(value=2, mask=0)
        imp4 = Implicant(value=3, mask=1)

        assert imp1.is_equal(imp2) is True
        assert imp1.is_equal(imp3) is False
        assert imp1.is_equal(imp4) is False

    def test_covers(self):
        # implicant "10-" (value=4, mask=1) -> покрывает 100 (4) и 101 (5)
        imp = Implicant(value=4, mask=1)
        assert imp.covers(4) is True
        assert imp.covers(5) is True
        assert imp.covers(6) is False
        assert imp.covers(0) is False


# ==========================================
# Тесты для qm.py (Quine-McCluskey)
# ==========================================
class TestQM:
    def test_differ_by_one_bit(self):
        # 000 и 001 отличаются на 1 бит (маски одинаковые)
        imp1 = Implicant(value=0, mask=0)
        imp2 = Implicant(value=1, mask=0)
        can_merge, merged = qm.differ_by_one_bit(imp1, imp2)
        assert can_merge is True
        assert merged.value == 0
        assert merged.mask == 1

        # Различаются более чем на 1 бит (000 и 011)
        imp3 = Implicant(value=3, mask=0)
        can_merge, merged = qm.differ_by_one_bit(imp1, imp3)
        assert can_merge is False

        # Разные маски
        imp4 = Implicant(value=0, mask=1)
        can_merge, merged = qm.differ_by_one_bit(imp1, imp4)
        assert can_merge is False

    def test_generate_sdnf(self):
        vars_names = ["A", "B"]
        # Пустой список минтермов
        assert qm.generate_sdnf(2, [], vars_names) == "0"
        
        # Минтермы 1 (01) и 3 (11)
        sdnf = qm.generate_sdnf(2, [1, 3], vars_names)
        assert sdnf == "(!A & B) | (A & B)"

    def test_minimize_empty(self):
        assert qm.minimize(2, [], [], ["A", "B"]) == "0"

    def test_minimize_full_cover(self):
        # 2 переменные, минтермы 0, 1, 2, 3 -> всегда 1
        assert qm.minimize(2, [0, 1, 2, 3], [], ["A", "B"]) == "1"

    def test_minimize_with_dont_cares(self):
        # Минтерм 3 (11), don't care 1 (01)
        # Суммарно могут схлопнуться в -1 (т.е. просто B)
        res = qm.minimize(2, [3], [1], ["A", "B"])
        assert res == "(B)"

    def test_minimize_complex(self):
        # Как в сумматоре: [1, 2, 4, 7]
        res = qm.minimize(3, [1, 2, 4, 7], None, ["X1", "X2", "X3"])
        assert "(!X1 & !X2 & X3)" in res
        assert "(X1 & X2 & X3)" in res

    def test_internal_append_unique(self):
        # Покрытие приватной функции для 100%
        items = [Implicant(1, 0)]
        new_items = qm._append_unique(items, Implicant(1, 0))
        assert len(new_items) == 1  # не добавился дубликат
        
        new_items2 = qm._append_unique(items, Implicant(2, 0))
        assert len(new_items2) == 2  # добавился новый


# ==========================================
# Тесты для circuits.py
# ==========================================
class TestCircuits:
    @pytest.mark.parametrize("value, expected_val, expected_valid", [
        (0, 0, True),
        (4, 4, True),
        (8, 5, True),
        (12, 9, True),
        (5, -1, False),
        (15, -1, False),
    ])
    def test_decode_5421(self, value, expected_val, expected_valid):
        val, is_valid = circuits.decode_5421(value)
        assert val == expected_val
        assert is_valid == expected_valid

    @pytest.mark.parametrize("value, expected", [
        (0, 0),
        (4, 4),
        (5, 8),
        (9, 12),
        (15, 0), # Неизвестное значение отдает default 0
    ])
    def test_encode_5421(self, value, expected):
        assert circuits.encode_5421(value) == expected

    def test_get_adder_equations(self):
        eqs = circuits.get_adder_equations()
        assert len(eqs) == 2
        assert eqs[0].name == "S (Сумма)"
        assert eqs[1].name == "Cout (Перенос)"
        assert len(eqs[0].minimized) > 0

    def test_get_decoder_5421_equations(self):
        eqs = circuits.get_decoder_5421_equations()
        assert len(eqs) == 4
        names = [eq.name for eq in eqs]
        assert names == ["O3", "O2", "O1", "O0"]

    def test_get_bcd_adder_equations(self):
        eqs = circuits.get_bcd_adder_equations()
        assert len(eqs) == 5
        names = [eq.name for eq in eqs]
        assert names == ["S4", "S3", "S2", "S1", "S0"]

    def test_get_encoder_5421_equations_offset_n(self):
        eqs = circuits.get_encoder_5421_equations_offset_n()
        assert len(eqs) == 8
        names = [eq.name for eq in eqs]
        assert names == ["T3", "T2", "T1", "T0", "U3", "U2", "U1", "U0"]

    def test_get_counter_equations(self):
        eqs = circuits.get_counter_equations()
        assert len(eqs) == 3
        names = [eq.name for eq in eqs]
        assert names == ["T2", "T1", "T0"]


# ==========================================
# Тесты для main.py
# ==========================================
class TestMain:
    def test_print_equations(self, capsys):
        # Тестируем вспомогательную функцию печати
        eqs = [Equation(name="Test", sdnf="SDNF_STR", minimized="MIN_STR")]
        
        # Без SDNF
        main._print_equations("Title 1", eqs, False)
        captured = capsys.readouterr()
        assert "Title 1\nTest = MIN_STR\n\n" in captured.out
        
        # С SDNF
        main._print_equations("Title 2", eqs, True)
        captured = capsys.readouterr()
        assert "Title 2\nTest:\nSDNF: SDNF_STR\nMinimized: MIN_STR\n" in captured.out

    def test_main_execution(self, capsys):
        # Проверяем, что главная функция отрабатывает от начала до конца без крашей
        main.main()
        captured = capsys.readouterr()
        
        assert "ОДС-3" in captured.out
        assert "5421 BCD -> Двоичный" in captured.out
        assert "Сумматор 5421 + 5421 -> двоичная сумма" in captured.out
        assert "Двоичный -> 5421 BCD" in captured.out
        assert "Двоичный счетчик вычитающего типа" in captured.out