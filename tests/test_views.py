import pytest
from unittest.mock import Mock, patch
import datetime
from src.views import greeting, exchange_rate, share_price, card_info


@patch('src.views.datetime.datetime')
def test_greeting_morning(mock_datetime):
    """Тест приветствия"""
    mock_datetime.now.return_value = datetime.datetime(2024, 1, 1, 8, 0, 0)
    assert greeting() == "Доброе утро"


@patch('requests.get')
def test_exchange_rate(mock_get, currencies, answer_currencies):
    """Тест при получении ответа от API"""
    mock_get.return_value.json.return_value = answer_currencies
    mock_get.return_value.status_code = 200
    assert exchange_rate(currencies) == [{'currency': 'USD', 'rate': 92.86}]


@patch('requests.get')
def test_exchange_rate_with_incorrect_status_code(mock_get, currencies, answer_currencies):
    """Тест при отсутствии ответа от API"""
    mock_get.return_value.json.return_value = answer_currencies
    mock_get.return_value.status_code = 404
    assert exchange_rate(currencies) == []


@patch('requests.get')
def test_share_price(mock_get, stocks, answer_stocks):
    """Тест при получении ответа от API"""
    mock_get.return_value.json.return_value = answer_stocks
    mock_get.return_value.status_code = 200
    assert exchange_rate(stocks) == [{"stock": "AAPL",
                                      "price": 221.19}]


@patch('requests.get')
def test_share_price_with_incorrect_status_code(mock_get, stocks, answer_stocks):
    """Тест при отсутствии ответа от API"""
    mock_get.return_value.json.return_value = answer_stocks
    mock_get.return_value.status_code = 404
    assert exchange_rate(stocks) == []


def test_card_info(test_df):
    """Тест корректности работы функции"""
    assert card_info("2021-12-31 16:44:00", test_df) == [
        {'Card number': '5091', 'Transaction amount': -564.0, 'cashback': 5.64},
        {'Card number': '7197', 'Transaction amount': -344.33, 'cashback': 3.44}]


def test_card_info_incorrect_date(test_df):
    """Тест функции с некорректным форматом даты"""
    assert card_info("21.12.2021 16:44:00", test_df) == []



