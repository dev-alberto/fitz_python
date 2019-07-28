import pandas as pd
import numpy as np

from raw_data_container import Raw
from util import get_datetime_from_miliseconds
from numpy_ringbuffer import RingBuffer


# reporpose this to a Raw data manager of sorts.. Move feature building to another class
# probably another class will need to be created in order to deal with updates on different time frames, different symbols etc...
# this should receive as params exchange symbol etc ... (hint, maybe the instance.js file should be used, as dependency injection of sorts)
class RawDataManager:

    def __init__(self, exchange, symbol, period, lookback, history):
        #self.DF = None

        self.exchange = exchange
        self.symbol = symbol
        self.period = period
        self.lookback = lookback

        self.history = history
        
        self.live_data = Raw()

        self.backfill_data = Raw()

    # returns a dict of raw data {'close':[], 'open':[] etc}, where arrays are numpy,
    # this is the format that is exposed,  for feature creation
    def get_live_data(self):
        r = {}
        for k,v in self.live_data.get_data().items():
            r[k] = np.array(v)

        return r

    def get_backfill_data(self):
        return self.backfill_data.get_data()

    def backfill(self, data):
        assert len(data) != 0

        time = []
        open = []
        high = []
        low = []
        close = []
        volume = []

        time_l = RingBuffer(capacity=self.lookback, dtype=object) 
        open_l = RingBuffer(capacity=self.lookback, dtype=np.float64) 
        high_l = RingBuffer(capacity=self.lookback, dtype=np.float64)
        low_l = RingBuffer(capacity=self.lookback, dtype=np.float64) 
        close_l = RingBuffer(capacity=self.lookback, dtype=np.float64) 
        volume_l = RingBuffer(capacity=self.lookback, dtype=np.float64)

        for idx, candle in enumerate(data):
            if (self.history - idx) <= self.lookback:
                time_l.append(get_datetime_from_miliseconds(candle.get('time')))
                open_l.append(candle.get('open'))
                high_l.append(candle.get('high'))
                low_l.append(candle.get('low'))
                close_l.append(candle.get('close'))
                volume_l.append(candle.get('volume'))

            time.append(get_datetime_from_miliseconds(candle.get('time')))
            open.append(candle.get('open'))
            high.append(candle.get('high'))
            low.append(candle.get('low'))
            close.append(candle.get('close'))
            volume.append(candle.get('volume'))
        
        self.live_data.set_time(time_l)
        self.live_data.set_open(open_l)
        self.live_data.set_close(close_l)
        self.live_data.set_high(high_l)
        self.live_data.set_low(low_l)
        self.live_data.set_volume(volume_l)

        self.backfill_data.set_time(np.array(time, dtype=object))
        self.backfill_data.set_open(np.array(open, dtype=np.float64))
        self.backfill_data.set_high(np.array(high, dtype=np.float64))
        self.backfill_data.set_low(np.array(low, dtype=np.float64))
        self.backfill_data.set_close(np.array(close, dtype=np.float64))
        self.backfill_data.set_volume(np.array(volume, dtype=np.float64))

        #print(len(self.raw.get_close()))

        #cc = self.raw.get_close()[-1:]
        tt = self.live_data.get_data().get('time')[-1:]

        print("Backfill last candle time: ")
        print(tt)
        
        #self.DF = self.create_df()

    def update(self, data):
        candle = data[0]

        self.live_data.update_time(get_datetime_from_miliseconds(candle.get('time')))
        self.live_data.update_open(candle.get('open'))
        self.live_data.update_high(candle.get('high'))
        self.live_data.update_low(candle.get('low'))
        self.live_data.update_close(candle.get('close'))
        self.live_data.update_volume(candle.get('volume'))


        tt = self.live_data.get_data().get('time')[-1:]

        print("Live candle time: ")
        print(tt)

    def get_lookback(self):
        return self.lookback

    def get_history(self):
        return self.history