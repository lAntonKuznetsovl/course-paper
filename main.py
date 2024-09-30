import json

import pandas as pd

from config import PATH_TO_FILE
from src.reports import average_cost_amount, spending_by_category, writing_report
from src.services import editing_date_format_for_investment_bank, investment_bank
from src.views import return_json_answer

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
    "The amount of the operation with rounding",
]
edited_df_from_investment_bank = df.drop(
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

data_list = edited_df_from_investment_bank.to_dict(orient="records")

with open("user_settings.json") as file:
    data_file = json.load(file)


def main(date: str, data_frame: pd.DataFrame):
    print(return_json_answer(data_frame, date, data_file))
    limit_for_rounding_investment_bank = int(input("Введите лимит округления суммы для Инвесткопилки: "))
    print(
        investment_bank(editing_date_format_for_investment_bank(date), data_list, limit_for_rounding_investment_bank)
    )
    category = input("Введите категорию для фильтрации транзакций: ")
    print(spending_by_category(data_frame, category, date).to_json(orient="records", indent=4, force_ascii=False))
    print(average_cost_amount(data_frame, date).to_json(orient="records", indent=4, force_ascii=False))


if __name__ == "__main__":
    date_str = input("Введите дату в формате: YYYY-MM-DD HH:MM:SS: ")
    print(main(date_str, df))
