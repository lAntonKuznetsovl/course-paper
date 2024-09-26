import pytest
from unittest.mock import patch
from src.views import greeting, exchange_rate, share_price, card_info, top_5_transactions


def test_greeting():
    """Тест приветствия"""
    assert greeting("2021-11-14 14:00:00") == "Добрый день"
    assert greeting("2021-11-14 01:00:00") == "Доброй ночи"
    assert greeting("2021-11-14 10:00:00") == "Доброе утро"
    assert greeting("2021-11-14 20:00:00") == "Добрый вечер"


@patch('src.views.requests.get')
def test_exchange_rate(mock_get, currencies, answer_currencies):
    """Тест при получении ответа от API"""
    mock_get.return_value.json.return_value = answer_currencies
    mock_get.return_value.status_code = 200
    assert exchange_rate(currencies) == [{'currency': 'USD', 'rate': 92.86}]


@patch('src.views.requests.get')
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
        {'Card number': '5091', 'Transaction amount': -1589.0, 'cashback': 15.89},
        {'Card number': '7197', 'Transaction amount': -344.33, 'cashback': 3.44}]


def test_card_info_incorrect_date_format(test_df):
    """Тест функции с некорректным форматом даты"""
    assert card_info("21.12.2021 16:44:00", test_df) == []


def test_top_5_transactions(test_df):
    """Тест топ 5 транзакций за месяц"""
    assert top_5_transactions("2021-12-31 16:44:00", test_df) == [
        {'date': '31.12.2021', 'amount': -564.0, 'category': 'Различные товары', 'description': 5411},
        {'date': '09.12.2021', 'amount': -525.0, 'category': 'Одежда и обувь', 'description': 5651},
        {'date': '16.12.2021', 'amount': -500.0, 'category': 'Местный транспорт', 'description': 4111},
        {'date': '31.12.2021', 'amount': -160.89, 'category': 'Супермаркеты', 'description': 5411},
        {'date': '31.12.2021', 'amount': -118.12, 'category': 'Супермаркеты', 'description': 5411}]


def test_top_5_transactions_with_incorrect_date_format(test_df):
    """Тест топа транзакций при некорректном формате даты"""
    assert top_5_transactions("2021.12.31 16:44:00", test_df) == []
