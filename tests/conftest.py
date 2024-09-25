import pytest
import pandas as pd
from typing import Any


@pytest.fixture
def currencies() -> dict[str, Any]:
    return {
        "user_currencies": ["USD"]

    }


@pytest.fixture
def answer_currencies() -> dict[str, Any]:
    return {
        "base": "USD",
        "date": "2022-04-14",
        "rates": {
            "RUB": 92.86
        },
        "success": True,
        "timestamp": 1519296206
    }


@pytest.fixture
def stocks() -> dict[str, Any]:
    return {
        "user_stocks": ["AAPL"]
    }


@pytest.fixture
def answer_stocks() -> dict[str, Any]:
    return {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "AAPL",
            "3. Last Refreshed": "2024-09-24",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2024-09-24": {
                "1. open": "219.7800",
                "2. high": "221.1900",
                "3. low": "218.1600",
                "4. close": "220.9700",
                "5. volume": "3184114"
            },
            "2024-09-23": {
                "1. open": "218.0000",
                "2. high": "220.6200",
                "3. low": "217.2700",
                "4. close": "220.5000",
                "5. volume": "4074755"
            }}}


@pytest.fixture
def test_df() -> pd.DataFrame:
    """Тестовый DataFrame"""
    test_dict = {
        "Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04", "31.12.2021 16:39:04", "31.12.2021 01:23:42",
                          "30.12.2021 19:06:39"],
        "Дата платежа": ["31.12.2021", "31.12.2021", "31.12.2021", "31.12.2021", "31.12.2021"],
        "Номер карты": ["*7197", "*7197", "*7197", "*5091", "*7197"],
        "Статус": ["OK", "OK", "OK", "OK", "OK"],
        "Сумма операции": [-160.89, -64.00, -118.12, -564, -1.32],
        "Валюта операции": ["RUB", "RUB", "RUB", "RUB", "RUB"],
        "Сумма платежа": [-160.89, -64.00, -118.12, -564, -1.32],
        "Валюта платежа": ["RUB", "RUB", "RUB", "RUB", "RUB"],
        "Кэшбэк": [None, None, None, None, 70],
        "Категория": ["Супермаркеты", "Супермаркеты", "Супермаркеты", "Различные товары", "Каршеринг"],
        "Описание": ["Колхоз", "Колхоз", "Магнит", "Константин. К", "Ситидрайв"],
        "МСС": [5411, 5411, 5411, 5411, 5411],
        "Бонусы (включая кэшбэк)": [3, 1, 2, 5, 0],
        "Округление на инвесткопилку": [0, 0, 0, 0, 0],
        "Сумма операции с округлением": [160.89, 64.00, 118.12, 564, 1.32],

    }
    return pd.DataFrame(test_dict)
