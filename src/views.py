import datetime
import logging
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_RATES_DATA_API = os.getenv("API_KEY_APILAYER")
API = os.getenv("API_KEY_ALPHA_VANTAGE")
PATH_TO_FILE = os.path.join(os.path.dirname(__file__), "../data", "operations.xlsx")
df = pd.read_excel(PATH_TO_FILE)


# Настройки логера
views_logger = logging.getLogger("views")
file_handler = logging.FileHandler("logs/views.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
views_logger.addHandler(file_handler)
views_logger.setLevel(logging.INFO)


def greeting(date: str) -> str:
    """Функция вывода сообщения приветствия в зависимости от времени суток"""
    opts = {"greeting": ("Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи")}
    current_time = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    if 4 <= current_time.hour <= 12:
        greet = opts["greeting"][0]
    elif 12 <= current_time.hour <= 16:
        greet = opts["greeting"][1]
    elif 16 <= current_time.hour <= 24:
        greet = opts["greeting"][2]
    else:
        greet = opts["greeting"][3]
    return greet


def exchange_rate(currency_list: list[str]) -> list[dict[str, [str | int]]]:
    """Функция получения курса валют через API"""
    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": f"{EXCHANGE_RATES_DATA_API}"}
    currency_rate = []
    for currency in currency_list:
        payload = {"symbols": "RUB", "base": f"{currency}"}
        response = requests.get(url, headers=headers, params=payload)
        status_code = response.status_code
        if status_code == 200:
            res = response.json()
            currency_rate_dict = {"currency": f"{res["base"]}", "rate": round(float(res["rates"]["RUB"]), 2)}
            currency_rate.append(currency_rate_dict)
        else:
            print("Запрос не был успешным.")
            views_logger.warning("Запрос не удался")
            return []
    views_logger.info("Данные по курсу валют успешно получены")
    return currency_rate


def share_price(stock_list: list[str]) -> list[dict[str, [str | int]]]:
    """Функция получающая курс акций"""
    stocks_rate = []
    for stock in stock_list:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API}"
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            res = response.json()
            new_dict = {
                "stock": stock,
                "price": round(
                    float(
                        res["Time Series (Daily)"][
                            (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                        ]["2. high"]
                    ),
                    2,
                ),
            }
            stocks_rate.append(new_dict)
        else:
            views_logger.info("Произошла ощибка")
            print("Произошла ошибка")
    views_logger.info("Данные по курсу акций успешно получены")
    return stocks_rate


def card_info(date_string: str, DataFrame: pd.DataFrame) -> list[dict[str, Any]]:
    """Функция отображения информации о карте в заданном формате"""
    try:
        date_string_dt_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
        start_date_for_sorting = date_string_dt_obj.replace(day=1)
        DataFrame.columns = [
            "Transaction date",
            "Payment date",
            "Card number",
            "Status",
            "Transaction amount",
            "Transaction currency",
            "Payment amount",
            "Payment currency",
            "Cashback",
            "Category",
            "MCC",
            "Description",
            "Bonuses (including cashback)",
            "Rounding to the investment bank",
            "The amount of the operation with rounding",
        ]
        edited_df = DataFrame.drop(
            [
                "Payment date",
                "Transaction currency",
                "Payment amount",
                "Payment currency",
                "Cashback",
                "Category",
                "MCC",
                "Description",
                "Bonuses (including cashback)",
                "Rounding to the investment bank",
                "The amount of the operation with rounding",
            ],
            axis=1,
        )
        edited_df["Transaction date"] = edited_df["Transaction date"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        filtered_df_by_date = edited_df.loc[
            (edited_df["Transaction date"] <= date_string_dt_obj)
            & (edited_df["Transaction date"] >= start_date_for_sorting)
            & (edited_df["Card number"].notnull())
            & (edited_df["Transaction amount"] <= 0)
            & (edited_df["Status"] != "FAILED")
            ]
        grouped_df = filtered_df_by_date.groupby(["Card number"], as_index=False).agg({"Transaction amount": "sum"})
        data_list = []
        for index, row in grouped_df.iterrows():
            data_dict = {
                "Card number": row["Card number"].replace("*", ""),
                "Transaction amount": round(row["Transaction amount"], 2),
                "cashback": abs(round(row["Transaction amount"] / 100, 2)),
            }
            data_list.append(data_dict)
        views_logger.info("Данные по картам успешно сформированны")
        return data_list
    except ValueError:
        print("Неверный формат даты")
        views_logger.error("Ошибка ввода данных: неверный формат даты")
        return []


def top_5_transactions(date_string: str, DataFrame: pd.DataFrame) -> list[dict[str, Any]]:
    """Функция отображения топ 5 транзакций по сумме платежа"""
    try:
        date_string_dt_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
        start_date_for_sorting = date_string_dt_obj.replace(day=1)
        DataFrame.columns = [
            "Transaction date",
            "Payment date",
            "Card number",
            "Status",
            "Transaction amount",
            "Transaction currency",
            "Payment amount",
            "Payment currency",
            "Cashback",
            "Category",
            "MCC",
            "Description",
            "Bonuses (including cashback)",
            "Rounding to the investment bank",
            "The amount of the operation with rounding",
        ]
        edited_df = DataFrame.drop(
            [
                "Payment date",
                "Card number",
                "Transaction currency",
                "Payment amount",
                "Payment currency",
                "Cashback",
                "MCC",
                "Bonuses (including cashback)",
                "Rounding to the investment bank",
                "The amount of the operation with rounding",
            ],
            axis=1,
        )
        edited_df["Transaction date"] = edited_df["Transaction date"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        filtered_df_by_date = edited_df.loc[
            (edited_df["Transaction date"] <= date_string_dt_obj)
            & (edited_df["Transaction date"] >= start_date_for_sorting)
            & (edited_df["Transaction amount"].notnull())
            & (edited_df["Status"] != "FAILED")
            ]
        sorted_df_by_transaction_amount = filtered_df_by_date.sort_values(
            by=["Transaction amount"], ascending=False, key=lambda x: abs(x)
        )
        top_transactions = sorted_df_by_transaction_amount[0:5]
        data_list = []
        for index, row in top_transactions.iterrows():
            data_dict = {
                "date": row["Transaction date"].strftime("%d.%m.%Y"),
                "amount": round(row["Transaction amount"], 2),
                "category": row["Category"],
                "description": row["Description"],
            }
            data_list.append(data_dict)
        views_logger.info("Данные по топу транзакций успешно сформированны")
    except ValueError:
        views_logger.error("Ошибка ввода данных: неверный формат даты")
        print("Неверный формат даты")
        return []
    else:
        return data_list


if __name__ == "__main__":
    print(card_info("2021-11-14 14:46:24", df))
