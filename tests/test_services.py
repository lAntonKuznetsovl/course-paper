import pytest

from src.services import editing_date_format_for_dataframe, editing_date_format_for_investment_bank, investment_bank


def test_investment_bank(test_list_for_investment_bank):
    """Тест расчёта инвесткопилки"""
    assert (
        investment_bank("2021-12", test_list_for_investment_bank, 50)
        == '{\n    "Investment bank": {\n        "2021-12": 87.11\n    }\n}'
    )


def test_investment_bank_with_incorrect_format_date(test_list_for_investment_bank):
    """Тест расчёта инвесткопилки с неверным форматом даты"""
    assert investment_bank("31.12.2021", test_list_for_investment_bank, 50) == 0


def test_printing_message(capsys, test_list_for_investment_bank):
    """Тест вывода сообщенгия при ошибке в формате даты"""
    investment_bank("2021-12-31", test_list_for_investment_bank, 50)
    result = capsys.readouterr()
    assert result.out == "Некорректный формат даты\n"


def test_editing_date_format_for_dataframe():
    """Тест корректности перевода формата даты"""
    assert editing_date_format_for_dataframe("31.12.2021 16:44:00") == "2021-12"


def test_editing_date_format_for_dataframe_with_incorrect_format(capsys):
    """Тест вывода сообщения при некорректном формате даты"""
    editing_date_format_for_dataframe("31-12-2021 16:44:00")
    result = capsys.readouterr()
    assert result.out == "Неверный формат даты\n"


def test_editing_date_format_for_investment_bank():
    """Тест корректности перевода формата даты для инвесткопилки"""
    assert editing_date_format_for_investment_bank("2021-11-14 14:46:24") == "2021-11"


def test_editing_date_format_for_investment_bank_with_incorrect_format(capsys):
    """Тест вывода сообщения при некорректном формате даты"""
    editing_date_format_for_dataframe("31-12-2021 16:44:00")
    result = capsys.readouterr()
    assert result.out == "Неверный формат даты\n"
