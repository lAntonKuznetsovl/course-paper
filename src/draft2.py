from functools import wraps
from typing import Optional, Callable, Any
import pandas as pd
import datetime
import json
import os


# PATH_TO_FILE = os.path.join(os.path.dirname(__file__), "../data", "operations.xlsx")
# df = pd.read_excel(PATH_TO_FILE)
# df.columns = [
#     "Transaction date",
#     "Payment date",
#     "Card number",
#     "Status",
#     "Transaction amount",
#     "Transaction currency",
#     "Payment amount",
#     "Payment currency",
#     "Cashback",
#     "Category",
#     "MCC",
#     "Description",
#     "Bonuses (including cashback)",
#     "Rounding to the investment bank",
#     "The amount of the operation with rounding"
# ]
#
#
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


#
#
# def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
#     """Функция выводящая траты за последние 3 месяца от вводимой даты в заданой категории"""
#     edited_df = transactions.drop(
#         ["Payment date",
#          "Card number",
#          "Status",
#          "Transaction currency",
#          "Payment amount",
#          "Payment currency",
#          "Cashback",
#          "MCC",
#          "Description",
#          "Bonuses (including cashback)",
#          "Rounding to the investment bank",
#          "The amount of the operation with rounding"
#          ],
#         axis=1,
#     )
#     edited_df["Transaction date"] = edited_df["Transaction date"].apply(
#         lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date())
#     try:
#         if date:
#             end_date_obj = datetime.datetime.strptime(date, "%d.%m.%Y").date()
#             start_date_obj = end_date_obj - datetime.timedelta(days=90)
#         else:
#             end_date_obj = datetime.datetime.now().date()
#             start_date_obj = end_date_obj - datetime.timedelta(days=90)
#         report_df = edited_df.loc[(edited_df["Transaction date"] <= end_date_obj) &
#                                   (edited_df["Transaction date"] >= start_date_obj) &
#                                   (edited_df["Category"] == category)]
#         report_df.loc[:, 'Transaction date'] = report_df['Transaction date'].apply(
#             lambda x: x.strftime("%d.%m.%Y")
#         )
#     except ValueError as e:
#         print(e)
#         print('Неверный формат даты')
#     except NameError:
#         print('Некорректно указана категория')
#     else:
#         return report_df
#     finally:
#         print('Формирование отчёта завершено')
#
#
# print(spending_by_category(df, 'Супермаркеты', '31.12.2021'))
#
#
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
