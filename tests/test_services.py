import pytest

from src.services import investment_bank


def test_investment_bank(test_list_for_investment_bank):
    """Тест расчёта инвесткопилки"""
    assert investment_bank("2021-12", test_list_for_investment_bank, 50) == 87.11


def test_investment_bank_with_incorrect_format_date(test_list_for_investment_bank):
    """Тест расчёта инвесткопилки с неверным форматом даты"""
    assert investment_bank("2021-12-31", test_list_for_investment_bank, 50) == 0


def test_printing_message(capsys, test_list_for_investment_bank):
    """Тест вывода сообщенгия при ошибке в формате даты"""
    investment_bank("2021-12-31", test_list_for_investment_bank, 50)
    result = capsys.readouterr()
    assert result.out == "Некорректный формат даты\n"
