import requests
import json
from config import keys

class ConversionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException(f'Зачем вы это делаете??? {base} = {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'{quote} - отсутствует в списке доступных валют.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'{base} - отсутствует в списке доступных валют.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException('Введите число.')

        if float(amount) <= 0:
            raise ConversionException('Число должно быть больше 0.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = round(json.loads(r.content)[keys[base]] * float(amount), 2)

        return total_base
