import json
import requests
from config import values


class APIException(Exception):
    pass


class Exchanger:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            first_values = values[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не поддерживается")

        try:
            second_values = values[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не поддерживается")

        if first_values == second_values:
            raise APIException(f"Невозможно конвертировать одинаковые валюты {base}")

        try:
            amount_values = float(amount)
        except ValueError:
            raise APIException(f"Количество {amount} указано неверно")

        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={second_values}&base={first_values}"

        headers = {"apikey": "r6Jfoz4sLf8FVrRVwkWGlEM9IboTd1am"}

        r = requests.request("GET", url, headers=headers)
        response = json.loads(r.content)
        place_price = response['rates'][second_values] * amount_values
        place_price = round(place_price, 3)
        message = f"Цена {amount} {base} в {quote} : {place_price}"
        return message


