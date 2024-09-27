import pytest

from src.utils import editing_date_format


def test_editing_date_format():
    """Тест корректности перевода формата даты"""
    assert editing_date_format("31.12.2021 16:44:00") == "2021-12"


def test_editing_date_with_incorrect_format():
    """Тест при некорректном формате даты"""
    with pytest.raises(ValueError):
        editing_date_format("31-12-2021 16:44:00")
