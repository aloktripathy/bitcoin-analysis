import pytz
import datetime
from bottle import route, run, request

import settings
import utils
from models import Tick

HOST = 'localhost'
PORT = 8080
DEFAULT_DURATION = 60 * 60


@route('/ticks/<exchange>/<crypto_currency>/<exchange_currency>')
def ticks(exchange, crypto_currency, exchange_currency):
    cursor = Tick.objects.filter(
        exchange_name=exchange,
        crypto_currency=crypto_currency,
        exchange_currency=exchange_currency
    )

    # Fetch end timestamp from query params. If not specified, use current time.
    end_timestamp = request.GET.get('end', utils.get_now_timestamp())
    end_time = utils.get_utc_time_from_timestamp(int(end_timestamp))

    duration = request.GET.get('duration', DEFAULT_DURATION)
    start_time = end_time - datetime.timedelta(seconds=int(duration))

    cursor = cursor.filter(
        time__gte=start_time,
        time__lt=end_time
    ).order_by('-time').only('time', 'buy_price', 'sell_price')

    data = {
        'exchange': exchange,
        'crypto_currency': crypto_currency,
        'exchange_currency': exchange_currency,
        'ticks': []
    }
    for idx, doc in enumerate(cursor):
        doc.time = doc.time.replace(tzinfo=pytz.utc)
        row = dict(time=str(doc.time), buy=doc.buy_price, sell=doc.sell_price)
        data['ticks'].append(row)

    return data

run(host=HOST, port=PORT, reloader=True)
