import json
import requests

import constants


def get_zebpay_ticker(exchange_currency):
    url = constants.EXCHANGE_URLS[constants.EXCHANGE_ZEBPAY].format(exchange_currency)
    data = requests.get(url)
    return json.loads(data.text)


def get_through_bit_ticker(crypto_currency, exchange_currency):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
        'authority': 'www.throughbit.com',
        'upgrade-insecure-requests': '1'
    })
    url = constants.EXCHANGE_URLS[constants.EXCHANGE_THROUGH_BIT].format(
        crypto_currency,
        exchange_currency
    )
    print(url)
    data = requests.get(url, headers=headers)
    print(data.text)
    data = json.loads(data.text)
    if data:
        return data['data'][0]

    return None
