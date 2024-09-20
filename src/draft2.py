from functools import wraps
from typing import Optional, Callable, Any
import pandas as pd
import datetime
from config import PATH_TO_FILE
import json

df = pd.read_excel(PATH_TO_FILE)
df.columns = [
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
    "The amount of the operation with rounding"
]


def writing_report(filename: str) -> Callable:
    """Декоратор отвечающий за место вывода логов работы функции"""

    def my_decorator(function: Callable) -> Callable:
        """Декоратор записи данных в файл"""

        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            """Функция - обёртка"""
            # try:
            result = function(*args, **kwargs)
            if isinstance(filename, (str, int)):
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(result)

        #                 else:
        #                     raise TypeError
        #             except TypeError:
        #                 print('Название файла должно содержать только буквы и цифры')

        return inner

    return my_decorator


# @writing_report('report')
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция выводящая траты за последние 3 месяца от вводимой даты в заданой категории"""
    edited_df = transactions.drop(
        ["Payment date",
         "Card number",
         "Status",
         "Transaction currency",
         "Payment amount",
         "Payment currency",
         "Cashback",
         "MCC",
         "Description",
         "Bonuses (including cashback)",
         "Rounding to the investment bank",
         "The amount of the operation with rounding"
         ],
        axis=1,
    )
    edited_df["Transaction date"] = edited_df["Transaction date"].apply(
        lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date())
    try:
        if date:
            end_date_obj = datetime.datetime.strptime(date, "%d.%m.%Y").date()
            start_date_obj = end_date_obj - datetime.timedelta(days=90)
        else:
            end_date_obj = datetime.datetime.now().date()
            start_date_obj = end_date_obj - datetime.timedelta(days=90)
        report_df = edited_df.loc[(edited_df["Transaction date"] <= end_date_obj) &
                                  (edited_df["Transaction date"] >= start_date_obj) &
                                  (edited_df["Category"] == category)]
        report_df.loc[:, 'Transaction date'] = report_df['Transaction date'].apply(
            lambda x: x.strftime("%d.%m.%Y")
        )
        result = report_df.to_dict(orient='records')
        if not result:
            raise NameError
    except ValueError as e:
        print(e)
        print('Неверный формат даты')
    except NameError:
        print('Некорректно указана категория')
    else:
        report = report_df.to_json('report.json', orient='records', indent=4, lines=True)
        return report
    finally:
        print('Формирование отчёта завершено')


print(spending_by_category(df, 'Супермаркеты', '31.12.2021'))
