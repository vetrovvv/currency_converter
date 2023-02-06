import requests
import json

from config import keys


class ConvertionException(Exception):
    pass


class NegativeException(ConvertionException):
    def __init__(self, amount):
        self.amount = amount


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: int):
        if quote == base:
            raise ConvertionException(f'Невозможно сконвертировать одинаковые валюты "{base}"!')
        try:
            keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалость обработать валюту {quote}!')
        try:
            base_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалость обработать валюту {base}!')
        try:
            amount == float(amount)
        except ValueError:
            raise ConvertionException(f'Невозможно обработать не целое число {amount}!')

        try:
            amount == str(amount)
        except ValueError:
            raise ConvertionException(f"Введена строка {amount} вместо числа!")

        try:
            amount = int(amount)
            if amount <= 0:
                raise NegativeException("Отрицательное число или 0! Повторите запрос!")
        except ValueError:
            pass

        quote_ticker, base_ticker = keys[quote], keys[base]
        r = requests.get(
            f'https://free.currconv.com/api/v7/convert?q={quote_ticker}_{base_ticker}&compact=ultra&apiKey'
            f'=26dba0ed3428f31be13c')
        currency_dict = json.loads(r.content)
        valuesList = []
        for key in currency_dict:
            valuesList.append(currency_dict[key])
        r = float("".join(str(x) for x in valuesList))
        amount = int(amount)
        result = r * amount
        return result
