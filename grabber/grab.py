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


grab_zebpay_ticker(constants.CURRENCY_INR)
grab_zebpay_ticker(constants.CURRENCY_USD)
