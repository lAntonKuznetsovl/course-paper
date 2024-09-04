import json
import requests
from dotenv import load_dotenv
import os

PATH_TO_FILE = os.path.join(os.path.dirname(__file__), "../data", "operations.xlsx")

load_dotenv()

API = os.getenv('API_KEY_ALPHA_VANTAGE')


# current_time = datetime.datetime.now()
# date_string = current_time.strftime("%Y-%m-%dT%H:%M:%S+0000")
# def editing_date(date_string: str) -> str:
#     """Функция приводящая дату к нужному формату"""
#     dt_obj = datetime.datetime.strptime(date_string, '%d.%m.%Y %H:%M:%S')
#     fixed_date_string = dt_obj.strftime('%d.%m.%Y')
#     return fixed_date_string
#
def share_price(stock_list: list[str]) -> dict[str, [str | int]]:
    stocks_rate = []
    for stock in stock_list:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API}'
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            res = response.json()
            return res
        else:
            print('Произошла ошибка')
            return []


with open('../user_settings.json', encoding='UTF-8') as file:
    data_dict = json.load(file)
stocks_list = share_price(data_dict['user_stocks'])
print(stocks_list)
