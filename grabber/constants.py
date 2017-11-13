EXCHANGE_ZEBPAY = 'zebpay'
EXCHANGE_THROUGH_BIT = 'through-bit'
EXCHANGE_COINBASE = 'coinbase'
EXCHANGE_COIN_SECURE = 'coin-secure'

CURRENCY_BITCOIN = 'btc'
CURRENCY_INR = 'inr'
CURRENCY_USD = 'usd'

EXCHANGE_URLS = {
    EXCHANGE_ZEBPAY: 'https://api.zebpay.com/api/v1/ticker?currencyCode={}',
    EXCHANGE_THROUGH_BIT: 'https://www.throughbit.com/tbit_ci/index.php/cryptoprice/type/{}/{}',
    EXCHANGE_COINBASE: 'https://api.coinbase.com/v2/prices/{}-{}/{}',
    EXCHANGE_COIN_SECURE: 'https://api.coinsecure.in/v1/exchange/ticker'
}

COLLECTION_TICKS = 'ticks'
