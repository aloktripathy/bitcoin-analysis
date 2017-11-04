import datetime
import pytz
import time


def get_utc_now():
    return pytz.utc.localize(datetime.datetime.utcnow())


def get_epoch_timestamp():
    return time.time()
