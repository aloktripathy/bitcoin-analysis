EXCHANGE_ZEBPAY = 'zebpay'
EXCHANGE_THROUGH_BIT = 'through-bit'

CURRENCY_BITCOIN = 'btc'
CURRENCY_INR = 'inr'
CURRENCY_USD = 'usd'

EXCHANGE_URLS = {
    EXCHANGE_ZEBPAY: 'https://api.zebpay.com/api/v1/ticker?currencyCode={}',
    EXCHANGE_THROUGH_BIT: 'https://www.throughbit.com/tbit_ci/index.php/cryptoprice/type/{}/{}'
}

COLLECTION_TICKS = 'ticks'
