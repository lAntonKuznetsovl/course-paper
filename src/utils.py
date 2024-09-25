import datetime


# Вспомогательная функция для services
def editing_date_format(date_string: str) -> str:
    """Функция приводящая дату к нужному формату"""
    date_string_dt_obj = datetime.datetime.strptime(date_string, "%d.%m.%Y %H:%M:%S").date()
    fixed_date = datetime.datetime.strftime(date_string_dt_obj, "%Y-%m")
    return fixed_date
