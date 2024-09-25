import json

import pandas as pd

from config import PATH_TO_FILE
from src.views import card_info, exchange_rate, greeting, top_5_transactions, share_price

df = pd.read_excel(PATH_TO_FILE)
with open("user_settings.json") as file:
    data_file = json.load(file)

date_str = input("Введите дату в формате: YYYY-MM-DD HH:MM:SS: ")


def return_json_answer(data_frame, date: str):
    """Главная функция выводящая результат запроса по дате"""
    info_by_transactions = {
        "greeting": greeting(),
        "cards": card_info(date, data_frame),
        "top transactions": top_5_transactions(date, data_frame),
        "currency rates": exchange_rate(data_file["user_currencies"]),
        "stock_prices": share_price(data_file["user_stocks"])
    }
    answer_in_json_format = json.dumps(info_by_transactions, indent=4, ensure_ascii=False)
    return answer_in_json_format


# print(return_json_answer(df, "2021-11-14 14:46:24"))
print(return_json_answer(df, date_str))
