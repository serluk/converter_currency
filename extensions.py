import json
import requests

from config import exchanges, headers, payload


class ApiException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise ApiException(f"Валюта {base} не найдена!")
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise ApiException(f"Валюта {base} не найдена!")

        try:
            amount = float(amount.replace(",", "."))
        except:
           raise ApiException(f"Не удалось обработать количество {amount}")

        r = requests.get(f"https://api.apilayer.com/fixer/convert?to={sym_key}&from={base_key}&amount={amount}",
                         headers=headers, data=payload)
        resp = json.loads(r.content)
        new_price = resp["result"]
        return new_price

