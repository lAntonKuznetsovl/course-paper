import pandas as pd
import datetime
from typing import Any, Optional, Callable
from functools import wraps
import json

test_dict = {
    "Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04", "31.12.2021 16:39:04", "31.12.2021 01:23:42",
                      "30.12.2021 19:06:39", "16.12.2021 11:26:30", "09.12.2021 08:50:35", "25.11.2021 20:29:13",
                      "19.11.2021 18:54:29", "28.10.2021 15:56:36", "16.09.2021 12:55:33"],
    "Дата платежа": ["31.12.2021", "31.12.2021", "31.12.2021", "31.12.2021", "31.12.2021", "18.12.2021",
                     "09.12.2021", "25.11.2021", "19.11.2021", "28.10.2021", "16.09.2021"],
    "Номер карты": ["*7197", "*7197", "*7197", "*5091", "*7197", "*5091", "*5091", "*4556", "*4556", "*7197",
                    "*7197"],
    "Статус": ["OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"],
    "Сумма операции": [-160.89, -64.00, -118.12, -564, -1.32, -500.00, -525.00, -681, -339.90, -1468.00, -110.00],
    "Валюта операции": ["RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB"],
    "Сумма платежа": [-160.89, -64.00, -118.12, -564, -1.32, -500.00, -525.00, -681, -339.90, -1468.00, -110.00],
    "Валюта платежа": ["RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB", "RUB"],
    "Кэшбэк": [None, None, None, None, 70, None, None, None, None, None, None],
    "Категория": ["Супермаркеты", "Супермаркеты", "Супермаркеты", "Различные товары", "Каршеринг",
                  "Местный транспорт", "Одежда и обувь", "Аптеки", "Супермаркеты", "Дом и ремонт", "Фастфуд"],
    "Описание": ["Колхоз", "Колхоз", "Магнит", "Константин. К", "Ситидрайв", "Метро Санкт-петербург", "WILDBERRIES",
                 "Аптека Вита", "Перекрёсток", "Леруа Мерлен", "Mouse Tail"],
    "МСС": [5411, 5411, 5411, 5411, 5411, 4111, 5651, 5912, 5411, 5200, 5814],
    "Бонусы (включая кэшбэк)": [3, 1, 2, 5, 0, 5, 5, 34, 16, 4, 2],
    "Округление на инвесткопилку": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Сумма операции с округлением": [160.89, 64.00, 118.12, 564, 1.32, 500.00, 525.00, 681, 339.90, 1468.00,
                                     110.00],

}
data = pd.DataFrame(test_dict)


def writing_report(filename: str) -> Callable:
    """Декоратор указывающий файл записи данных"""

    def my_decorator(function: Callable) -> Callable:
        """Декоратор записи данных в файл"""

        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            """Функция - обёртка"""
            result = function(*args, **kwargs)
            data = result.to_dict(orient="records")
            with open(f"{filename}.json", "w", encoding="UTF-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        return inner

    return my_decorator


# def card_info(date_string: str, DataFrame: pd.DataFrame) -> list[dict[str, Any]]:
#     """Функция отображения информации о карте в заданном формате"""
#     try:
#         date_string_dt_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
#         start_date_for_sorting = date_string_dt_obj.replace(day=1)
#         DataFrame.columns = [
#             "Transaction date",
#             "Payment date",
#             "Card number",
#             "Status",
#             "Transaction amount",
#             "Transaction currency",
#             "Payment amount",
#             "Payment currency",
#             "Cashback",
#             "Category",
#             "MCC",
#             "Description",
#             "Bonuses (including cashback)",
#             "Rounding to the investment bank",
#             "The amount of the operation with rounding",
#         ]
#         edited_df = DataFrame.drop(
#             [
#                 "Payment date",
#                 "Transaction currency",
#                 "Payment amount",
#                 "Payment currency",
#                 "Cashback",
#                 "Category",
#                 "MCC",
#                 "Description",
#                 "Bonuses (including cashback)",
#                 "Rounding to the investment bank",
#                 "The amount of the operation with rounding",
#             ],
#             axis=1,
#         )
#         edited_df["Transaction date"] = edited_df["Transaction date"].apply(
#             lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
#         )
#         filtered_df_by_date = edited_df.loc[
#             (edited_df["Transaction date"] <= date_string_dt_obj)
#             & (edited_df["Transaction date"] >= start_date_for_sorting)
#             & (edited_df["Card number"].notnull())
#             & (edited_df["Transaction amount"] <= 0)
#             & (edited_df["Status"] != "FAILED")
#             ]
#         grouped_df = filtered_df_by_date.groupby(["Card number"], as_index=False).agg({"Transaction amount": "sum"})
#         data_list = []
#         for index, row in grouped_df.iterrows():
#             data_dict = {
#                 "Card number": row["Card number"].replace("*", ""),
#                 "Transaction amount": round(row["Transaction amount"], 2),
#                 "cashback": abs(round(row["Transaction amount"] / 100, 2)),
#             }
#             data_list.append(data_dict)
#         # views_logger.info("Данные по картам успешно сформированны")
#         return data_list
#     except ValueError:
#         print("Неверный формат даты")
#         # views_logger.error("Ошибка ввода данных: неверный формат даты")
#
#
# print(card_info("2021-12-31 16:44:00", data))
# def top_5_transactions(date_string: str, DataFrame: pd.DataFrame) -> list[dict[str, Any]]:
#     """Функция отображения топ 5 транзакций по сумме платежа"""
#     try:
#         date_string_dt_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
#         start_date_for_sorting = date_string_dt_obj.replace(day=1)
#         DataFrame.columns = [
#             "Transaction date",
#             "Payment date",
#             "Card number",
#             "Status",
#             "Transaction amount",
#             "Transaction currency",
#             "Payment amount",
#             "Payment currency",
#             "Cashback",
#             "Category",
#             "MCC",
#             "Description",
#             "Bonuses (including cashback)",
#             "Rounding to the investment bank",
#             "The amount of the operation with rounding",
#         ]
#         edited_df = DataFrame.drop(
#             [
#                 "Payment date",
#                 "Card number",
#                 "Transaction currency",
#                 "Payment amount",
#                 "Payment currency",
#                 "Cashback",
#                 "MCC",
#                 "Bonuses (including cashback)",
#                 "Rounding to the investment bank",
#                 "The amount of the operation with rounding",
#             ],
#             axis=1,
#         )
#         edited_df["Transaction date"] = edited_df["Transaction date"].apply(
#             lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
#         )
#         filtered_df_by_date = edited_df.loc[
#             (edited_df["Transaction date"] <= date_string_dt_obj)
#             & (edited_df["Transaction date"] >= start_date_for_sorting)
#             & (edited_df["Transaction amount"].notnull())
#             & (edited_df["Status"] != "FAILED")
#             ]
#         sorted_df_by_transaction_amount = filtered_df_by_date.sort_values(
#             by=["Transaction amount"], ascending=False, key=lambda x: abs(x)
#         )
#         top_transactions = sorted_df_by_transaction_amount[0:5]
#         data_list = []
#         for index, row in top_transactions.iterrows():
#             data_dict = {
#                 "date": row["Transaction date"].strftime("%d.%m.%Y"),
#                 "amount": round(row["Transaction amount"], 2),
#                 "category": row["Category"],
#                 "description": row["Description"],
#             }
#             data_list.append(data_dict)
#         # views_logger.info("Данные по топу транзакций успешно сформированны")
#     except ValueError:
#         print("Неверный формат даты")
#         return []
#     else:
#         return data_list
#
#
# print(top_5_transactions("2021-12-31 16:44:00", data))


# def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
#     """Функция выводящая траты за последние 3 месяца от вводимой даты в заданой категории"""
#     transactions.columns = [
#         "Transaction date",
#         "Payment date",
#         "Card number",
#         "Status",
#         "Transaction amount",
#         "Transaction currency",
#         "Payment amount",
#         "Payment currency",
#         "Cashback",
#         "Category",
#         "MCC",
#         "Description",
#         "Bonuses (including cashback)",
#         "Rounding to the investment bank",
#         "The amount of the operation with rounding",
#     ]
#     edited_df = transactions.drop(
#         [
#             "Payment date",
#             "Card number",
#             "Status",
#             "Transaction currency",
#             "Payment amount",
#             "Payment currency",
#             "Cashback",
#             "MCC",
#             "Description",
#             "Bonuses (including cashback)",
#             "Rounding to the investment bank",
#             "The amount of the operation with rounding",
#         ],
#         axis=1,
#     )
#     edited_df["Transaction date"] = edited_df["Transaction date"].apply(
#         lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
#     )
#     try:
#         if date:
#             end_date_obj = datetime.datetime.strptime(date, "%d.%m.%Y").date()
#             start_date_obj = end_date_obj - datetime.timedelta(days=90)
#         else:
#             end_date_obj = datetime.datetime.now().date()
#             start_date_obj = end_date_obj - datetime.timedelta(days=90)
#         report_df = edited_df.loc[
#             (edited_df["Transaction date"] <= end_date_obj)
#             & (edited_df["Transaction date"] >= start_date_obj)
#             & (edited_df["Category"] == category)
#             ]
#         report_df.loc[:, "Transaction date"] = report_df["Transaction date"].apply(lambda x: x.strftime("%d.%m.%Y"))
#         if not report_df.to_dict(orient='records'):
#             raise NameError
#     except ValueError:
#         # reports_logger.error("Ошибка в выборке операций: не корректный формат даты")
#         print("Неверный формат даты")
#         return []
#     except NameError:
#         print("Неверно введена категория")
#         return []
#     else:
# #         reports_logger.info("Выборка операций успешно завершена")
#         return report_df
#     finally:
# #         reports_logger.info("Завершение работы программы")
#         print("Формирование отчёта завершено")

@writing_report("report")
def average_cost_amount(data_frame: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращающая среднее значение трат за день за последние 3 месяца от введённой даты"""
    data_frame.columns = [
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
    edited_df = data_frame.drop(
        [
            "Payment date",
            "Card number",
            "Status",
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
    try:
        if date:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        else:
            date = datetime.date.today()
        start_date_for_counting = date - datetime.timedelta(days=90)
        edited_df["Transaction date"] = edited_df["Transaction date"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        filtered_df = edited_df.loc[
            (edited_df["Transaction date"] <= date)
            & (edited_df["Transaction date"] >= start_date_for_counting)
            & (edited_df["Transaction amount"] < 0)
            ]
        grouped_df_by_date = filtered_df.groupby(["Transaction date"], as_index=False).agg(
            {"Transaction amount": "mean"}
        )
        grouped_df_by_date["Transaction amount"] = round(grouped_df_by_date["Transaction amount"], 2)
        grouped_df_by_date.loc[:, "Transaction date"] = grouped_df_by_date["Transaction date"].apply(
            lambda x: x.strftime("%d.%m.%Y")
        )
        # reports_logger.info("Подсчёт среднедневных трат завершён")
        return grouped_df_by_date
    except ValueError:
        #         reports_logger.error("Не корректно указанна дата")
        print("Введён не верный формат даты")
        return pd.DataFrame({})


average_cost_amount(data, "2021-12-31")
# new_dict = result.to_dict(orient="records")
# print(new_dict)
