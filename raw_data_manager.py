import pandas as pd
import numpy as np

from raw_data_container import Raw
from util import get_datetime_from_miliseconds
from numpy_ringbuffer import RingBuffer


# reporpose this to a Raw data manager of sorts.. Move feature building to another class
# probably another class will need to be created in order to deal with updates on different time frames, different symbols etc...
# this should receive as params exchange symbol etc ... (hint, maybe the instance.js file should be used, as dependency injection of sorts)
class RawDataManager:

    def __init__(self, exchange, symbol, period, lookback, history=None):
        # self.DF = None

        self.exchange = exchange
        self.symbol = symbol
        self.period = period
        self.lookback = lookback

        self.history = history
        
        self.live_data = Raw()

        self.backfill_data = Raw()

        self.live_candle = None

    # returns a dict of raw data {'close':[], 'open':[] etc}, where arrays are numpy,
    # this is the format that is exposed,  for feature creation
    def get_live_data(self):
        r = {}
        for k,v in self.live_data.get_data().items():
            r[k] = np.array(v)

        return r
    
    # should not be necessary
    def get_live_df(self):
        dd = self.get_live_data()
        df = pd.DataFrame.from_dict(dd)
        df.set_index('time', inplace=True)
        return df

    def get_backfill_df(self):
        dd = self.get_backfill_data()
        df = pd.DataFrame.from_dict(dd)
        df.set_index('time', inplace=True)
        return df

    # backtest purposes 
    def get_backfill_df_from(self, start_time):
        dd = self.get_backfill_df()

        return dd[(dd.index >= start_time)]

    # backtest purposes
    def get_backfill_df_between(self, start, end):
        dd = self.get_backfill_df()

        return dd[(dd.index >= start) & (dd.index <= end)]

    def get_backfill_data(self):
        return self.backfill_data.get_data()

    def get_latest(self):
        ll = self.get_live_data()
        return {k:v[-1] for (k,v) in ll.items()}

    def backfill(self, data):
        assert len(data) != 0
        if self.history is None:
            self.history = len(data)

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
                # time_l.append(get_datetime_from_miliseconds(candle.get('time')))
                time_l.append(candle.get('time'))
                open_l.append(candle.get('open'))
                high_l.append(candle.get('high'))
                low_l.append(candle.get('low'))
                close_l.append(candle.get('close'))
                volume_l.append(candle.get('volume'))

            # time.append(get_datetime_from_miliseconds(candle.get('time')))
            time.append(candle.get('time'))
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
        # tt = get_datetime_from_miliseconds(candle.get('time'))
        tt = candle.get('time')
        candle['time'] = tt

        self.live_candle = candle

        self.live_data.update_time(candle.get('time'))
        self.live_data.update_open(candle.get('open'))
        self.live_data.update_high(candle.get('high'))
        self.live_data.update_low(candle.get('low'))
        self.live_data.update_close(candle.get('close'))
        self.live_data.update_volume(candle.get('volume'))

    def sava_backfill_to_disk(self, path):
        df = self.get_backfill_df()
        df.to_csv(path) 

    def get_lookback(self):
        return self.lookback

    def get_history(self):
        return self.history

    def get_period(self):
        return self.period

    def get_period_in_minutes(self):
        per = self.get_period()
        if per == '1m':
            return 1
        elif per == '5m':
            return 5
        elif per == '15m':
            return 15
        elif per == '30m':
            return 30
        elif per == '1h':
            return 60
        elif per == '2h':
            return 120
        elif per == '4h':
            return 240
        elif per == '1d':
            return 1440
        elif per == '1w':
            return 10080

    def get_symbol(self):
        return self.symbol

    def get_live_candle(self):
        return self.live_candle

    def __eq__(self, other):
        assert isinstance(other, RawDataManager)
        return self.symbol == other.symbol and self.exchange == other.exchange and self.period == other.period
