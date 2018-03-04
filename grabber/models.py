from datetime import datetime

from mongoengine import Document
from mongoengine import DateTimeField
from mongoengine import StringField
from mongoengine import FloatField
from mongoengine import DictField


class Tick(Document):
    exchange_name = StringField()
    crypto_currency = StringField()
    exchange_currency = StringField()
    buy_price = FloatField()
    sell_price = FloatField()
    extra = DictField(default={})
    time = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            {'fields': ['exchange_name', 'crypto_currency', 'exchange_currency', '-time']}
        ]
    }
