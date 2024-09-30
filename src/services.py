import datetime
import json
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(BASE_DIR, "logs", "services.log")

services_logger = logging.getLogger("services")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
services_logger.addHandler(file_handler)
services_logger.setLevel(logging.INFO)


def editing_date_format_for_investment_bank(date_string: str) -> str:
    """Функция приводящая дату к нужному формату для инвесткопилки"""
    try:
        date_string_dt_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
        fixed_date = datetime.datetime.strftime(date_string_dt_obj, "%Y-%m")
        return fixed_date
    except ValueError:
        print("Неверный формат даты")


def editing_date_format_for_dataframe(date_string: str) -> str:
    """Функция приводящая дату к нужному формату для датафрейма"""
    try:
        date_string_dt_obj = datetime.datetime.strptime(date_string, "%d.%m.%Y %H:%M:%S").date()
        fixed_date = datetime.datetime.strftime(date_string_dt_obj, "%Y-%m")
        return fixed_date
    except ValueError:
        print("Неверный формат даты")


def investment_bank(month: str, transactions: list[dict[str, [str | float]]], limit: int):
    """Функция расчитывающая сумму отложенную в инвесткопилку для каждой транзакции"""
    transaction_list_for_month = []
    for element in transactions:
        if editing_date_format_for_dataframe(element["Transaction date"]) == month:
            transaction_list_for_month.append(element)
    try:
        if transaction_list_for_month:
            services_logger.info("Сортировка транзакций завершена")
            for transaction in transaction_list_for_month:
                if (
                    abs(transaction["Transaction amount"]) <= limit
                    and abs(transaction["Transaction amount"]) % limit != 0
                ):
                    amount_to_investbank = limit - abs(transaction["Transaction amount"])
                    amount_with_rounding = abs(transaction["Transaction amount"]) + amount_to_investbank
                    transaction["Rounding to the investment bank"] = round(amount_to_investbank, 2)
                    transaction["The amount of the operation with rounding"] = amount_with_rounding
                elif (
                    abs(transaction["Transaction amount"]) >= limit
                    and abs(transaction["Transaction amount"]) % limit != 0
                ):
                    amount_to_investbank = limit - abs(transaction["Transaction amount"]) % limit
                    amount_with_rounding = abs(transaction["Transaction amount"]) + amount_to_investbank
                    transaction["Rounding to the investment bank"] = round(amount_to_investbank, 2)
                    transaction["The amount of the operation with rounding"] = amount_with_rounding
                else:
                    transaction["Rounding to the investment bank"] = 0
                    transaction["The amount of the operation with rounding"] = transaction["Transaction amount"]
            services_logger.info("Расчёт кэшбека по каждой транзакции завершён успешно")
            total_sum_to_investment_bank = 0
            for element in transaction_list_for_month:
                total_sum_to_investment_bank += element["Rounding to the investment bank"]
            dict_for_json = {"Investment bank": {f"{month}": round(total_sum_to_investment_bank, 2)}}
            answer_in_json_format = json.dumps(dict_for_json, indent=4, ensure_ascii=False)
            return answer_in_json_format
        else:
            raise ValueError
    except ValueError:
        print("Некорректный формат даты")
        services_logger.error("Неверный формат даты")
        return 0
