import datetime
import pytz
import time


def utc_now():
    return pytz.utc.localize(datetime.datetime.utcnow())


def get_now_timestamp():
    return time.time()


def get_utc_time_from_timestamp(ts):
    epoch_time = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
    return epoch_time + datetime.timedelta(seconds=ts)
