from unittest.mock import patch

import pytest

from src.views import share_price


@patch("src.views.requests.get")
def test_share_price(mock_get, stocks, answer_stocks):
    """Тест при получении ответа от API"""
    mock_get.return_value.json.return_value = answer_stocks
    mock_get.return_value.status_code = 200
    assert share_price(stocks) == [{"stock": "AAPL", "price": 221.19}]


@patch("src.views.requests.get")
def test_share_price_with_incorrect_status_code(mock_get, stocks, answer_stocks):
    """Тест при отсутствии ответа от API"""
    mock_get.return_value.json.return_value = answer_stocks
    mock_get.return_value.status_code = 404
    assert share_price(stocks) == []
