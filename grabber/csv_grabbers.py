import csv
import requests
import time
import os
from abc import ABCMeta
from abc import abstractmethod
import json
import datetime


class BaseGrabber:
    __metaclass__ = ABCMeta

    # Contains the supported candle time-frames and their value in seconds.
    TIME_FRAMES = dict()
    # The source of data (name of exchange).
    SOURCE_NAME = 'UNNAMED'

    def __init__(self, time_frame, trade, batch_size, directory='', verbose=True,
                 sleep_duration=.0, is_ms=True, **kwargs):
        """Implement this base class to create grabbers.

        Args:
            time_frame (str): Candle time frame.
            trade (str): The trade index. e.g. - BTCUSD, ETHUSD, LTCUSD etc.
            batch_size (int):  The number of candles to be grabbed at once.
            directory (str): An existing directory where the csv file will be stored.
            verbose (bool): If true, then print data crawling status.
            sleep_duration (float): Time for which system will sleep between two consecutive grabs.
                Helpful for sources that have hard throttling.
            is_ms (bool): If true then time is interpreted in milli-seconds.
        """
        self._time_frame = time_frame
        self._trade = trade
        self._batch_size = batch_size
        self._directory = directory
        self._verbose = verbose
        self._sleep_duration = sleep_duration
        self._is_ms = is_ms

        if self._time_frame not in self.TIME_FRAMES:
            raise ValueError('{} is an invalid value for time_frame. Valid values: {}'.format(
                self.TIME_FRAMES,
                ', '.join(self._time_frame)
            ))
        self._time_frame_seconds = self.TIME_FRAMES[self._time_frame]

    def _get_now_time_rounded(self):
        """Return the current epoch timestamp."""
        t = time.time()
        # Round t to floor of modulo time_frame.
        t = int(t // self._time_frame_seconds * self._time_frame_seconds)
        if self._is_ms:
            t *= 1000
        return int(t)

    def _get_human_readable_time(self, timestamp):
        """Convert an integer timestamp to human readable format."""
        if self._is_ms:
            timestamp /= 1000
        t = datetime.datetime.fromtimestamp(timestamp)
        return t.strftime("%Y-%m-%d %H:%M")

    def _get_filename(self):
        """Return the name of the csv file where data will be stored."""
        filename = '{}-{}-{}.csv'.format(self.SOURCE_NAME, self._time_frame, self._trade)
        return os.path.join(self._directory, filename)

    @staticmethod
    def _get_candle_ts(candle):
        """Given a candle, return it's timestamp.

        Notes:
            - Assumes that candle object is a iterable with first element as the timestamp value.
        """
        return int(candle[0])

    @abstractmethod
    def _get_candles_from_exchange(self, end_ts, **kwargs):
        """Return batch_size no. of candles ending at end_ts in increasing order of time.

        Args:
            end_ts (int): The end timestamp until which candles will be grabbed.

        Returns:
            list: of tuples / lists in the format (timestamp, open, close, high, low, volume)
        """
        pass

    def _sleep(self):
        self._log('Sleeping for {} seconds'.format(self._sleep_duration))
        time.sleep(self._sleep_duration)

    def get_candles(self, start_ts=None, end_ts=None):
        """Return all candles between start_ts and end_ts in increasing order of time.

        Args:
            start_ts (int): The start time in seconds or milliseconds based of the is_ms property.
            end_ts (int): The end time until which candles will be grabbed.
        """
        all_candles = []
        if not end_ts:
            end_ts = self._get_now_time_rounded()
        if not start_ts:
            start_ts = 0
        t_ptr = end_ts
        time_frame = self._time_frame_seconds
        if self._is_ms:
            time_frame *= 1000
        while t_ptr > start_ts:
            candles = self._get_candles_from_exchange(t_ptr)
            if not candles:
                break
            # Here we prepend the candles we received as we are querying back in time.
            all_candles = candles + all_candles
            # self._log([self._get_human_readable_time(t_ptr),
            #            self._get_human_readable_time(start_ts),
            #            self._get_human_readable_time(self._get_candle_ts(candles[0]))])
            t_ptr = self._get_candle_ts(candles[0]) - time_frame
            self._sleep()
        return all_candles

    def generate_csv(self):
        """Create a csv by grabbing all candles available from the source."""
        candles = self.get_candles()
        filename = self._get_filename()
        self._log('Grabbed {} candles in total. Writing to file {}'.format(len(candles), filename))
        with open(filename, 'w', newline='') as fp:
            writer = csv.writer(fp)
            for row in candles:
                writer.writerow(row)

    def update_csv(self):
        """Update an existing csv with most recent candles."""
        filename = self._get_filename()
        if not os.path.isfile(filename):
            self.generate_csv()
            return

        last_candle = None
        with open(self._get_filename(), 'r', newline='') as fp:
            reader = csv.reader(fp)
            for row in reader:
                last_candle = row
        start_ts = self._get_candle_ts(last_candle)
        end_ts = self._get_now_time_rounded()
        candles = self.get_candles(start_ts, end_ts)
        self._log('Updating {} with {} candles.'.format(filename, len(candles)))
        with open(self._get_filename(), 'a') as fp:
            writer = csv.writer(fp)
            for row in candles:
                writer.writerow(row)

    def _log(self, message):
        if self._verbose:
            print(datetime.datetime.now(), '-', message)


class BitfinexGrabber(BaseGrabber):
    TIME_FRAMES = {
        '1m': 60,
        '5m': 60*5,
        '15m': 60*15,
        '30m': 60*30,
        '1h': 60*60,
        '3h': 60*60*3,
        '6h': 60*60*6,
        '12h': 60*60*12,
        '1D': 60*60*24
    }
    SOURCE_NAME = 'bitfinex'
    URL = 'https://api.bitfinex.com/v2/candles/trade:{t_frame}:t{trade}/hist?limit={limit}&end={ms}'

    def __init__(self, time_frame, trade, batch_size=1000, directory='', verbose=True,
                 sleep_duration=.0, is_ms=True, **kwargs):
        super().__init__(time_frame, trade, batch_size, directory, verbose,
                         sleep_duration, is_ms, **kwargs)

    def _get_candles_from_exchange(self, end_ts, **kwargs):
        url = self.URL.format(t_frame=self._time_frame, trade=self._trade, limit=self._batch_size,
                              ms=end_ts)
        resp = requests.get(url)
        candles = json.loads(resp.text)
        candles.sort(key=lambda candle: candle[0])
        self._log('Grabbed {} candles until {}'.format(
            len(candles),
            self._get_human_readable_time(end_ts)
        ))
        return candles

from collections import Counter

if __name__ == '__main__':
    g = BitfinexGrabber('5m', 'BTCUSD', 1000, sleep_duration=3, is_ms=True, verbose=True)
    g.generate_csv()
    candles = []
    with open('bitfinex-5m-BTCUSD.csv', newline='\n') as fp:
        r = csv.reader(fp)
        for row in r:
            candles.append(row)
    ts_list = [a[0] for a in candles]
    ts_divs = []
    for i in range(len(ts_list)-1):
        ts_divs.append(int(ts_list[i+1]) - int(ts_list[i]))

    c = Counter(ts_divs)
    print(c)
    print('indexes')
    for i in c.keys():
        print(ts_divs.index(i))
