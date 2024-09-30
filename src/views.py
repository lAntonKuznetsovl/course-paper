import json

import pandas as pd

from src.utils import card_info, exchange_rate, greeting, share_price, top_5_transactions


def return_json_answer(data_frame: pd.DataFrame, date: str, user_settings):
    """Главная функция выводящая результат запроса по дате"""
    info_by_transactions = {
        "greeting": greeting(),
        "cards": card_info(date, data_frame),
        "top transactions": top_5_transactions(date, data_frame),
        "currency rates": exchange_rate(user_settings["user_currencies"]),
        "stock_prices": share_price(user_settings["user_stocks"]),
    }
    answer_in_json_format = json.dumps(info_by_transactions, indent=4, ensure_ascii=False)
    return answer_in_json_format
