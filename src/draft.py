import pandas as pd
import datetime
from typing import Any

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
data = pd.DataFrame(test_dict)


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
        # views_logger.info("Данные по картам успешно сформированны")
        return data_list
    except ValueError:
        print("Неверный формат даты")
        # views_logger.error("Ошибка ввода данных: неверный формат даты")


print(card_info("2021-12-31 16:44:00", data))
