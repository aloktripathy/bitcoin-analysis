import settings
import constants
import vendors

from models import Tick


def grab_zebpay_ticker(currency):
    data = vendors.get_zebpay_ticker(currency)
    t = Tick(
        exchange_name=constants.EXCHANGE_ZEBPAY,
        crypto_currency=constants.CURRENCY_BITCOIN,
        exchange_currency=currency,
        buy_price=data.pop('buy'),
        sell_price=data.pop('sell'),
        extra=data
    )
    t.save()
    print(t.to_json())


def grab_through_bit_ticker(crypto_currency, exchange_currency):
    data = vendors.get_through_bit_ticker(crypto_currency, exchange_currency)
    t = Tick(
        exchange_name=constants.EXCHANGE_THROUGH_BIT,
        crypto_currency=crypto_currency,
        exchange_currency=exchange_currency,
        buy_price=data.pop('buy_price'),
        sell_price=data.pop('sell_price'),
        extra=data
    )
    t.save()


def grab_coinbase_ticker(crypto_currency, exchange_currency):
    data = vendors.get_coinbase_ticker(crypto_currency, exchange_currency)
    t = Tick(
        exchange_name=constants.EXCHANGE_COINBASE,
        crypto_currency=crypto_currency,
        exchange_currency=exchange_currency,
        buy_price=data.pop('buy_price'),
        sell_price=data.pop('sell_price'),
        extra=data
    )
    t.save()
    print(t.to_json())


def grab_coin_secure_ticker():
    data = vendors.get_coin_secure_ticker()
    data = data.get('message', {})
    if not data:
        return
    t = Tick(
        exchange_name=constants.EXCHANGE_COIN_SECURE,
        crypto_currency=constants.CURRENCY_BITCOIN,
        exchange_currency=constants.CURRENCY_INR,
        buy_price=data['ask'] / 100,
        sell_price=data['bid'] / 100,
    )
    t.save()


grab_zebpay_ticker(constants.CURRENCY_INR)
grab_coinbase_ticker(constants.CURRENCY_BITCOIN, constants.CURRENCY_USD)
grab_coin_secure_ticker()
