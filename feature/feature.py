from numpy_ringbuffer import RingBuffer
from collections.abc import Sequence

from collections import OrderedDict

import numpy as np
import pandas as pd


class EmptyFeature(Sequence):
    
    def __init__(self, lookback, raw_data_manager, backfill=True, history_lengh=None, features=None):
        raw_data_length = raw_data_manager.get_history()

        # kind of spaghetii logic here to for feature history length but the gist is this:
        # one may specify history length when instantiating or we can produce the maximum 
        # length given the data available
        feath = 0
        hh = raw_data_length

        if features is not None:
            feath = min([f.get_history_length() for f in features]) 
            hh = feath

        if history_lengh is None:
            self.history_lengh = hh - lookback + 1
        else:
            self.history_lengh = history_lengh
            
        self.lookback = lookback

        self.raw_data_manager = raw_data_manager

        # raw data must be able to fill history
        assert (self.history_lengh + lookback - 1) <= raw_data_length
        assert lookback <= raw_data_manager.get_lookback()

        self.feature = OrderedDict()

        self.feature_numpy = RingBuffer(capacity=self.history_lengh, dtype=np.float64)
        
        self.latest = None

        # a feature may contain multiple features
        self.features = features

        self.feature_df = raw_data_manager.get_backfill_df()
        
        # trim df
        drop_i = self.lookback
        if self.features is not None:
            if len(self.features) > 0:       
               drop_i = drop_i + max([f.get_lookback() for f in self.features]) -1

        self.feature_df = self.feature_df.iloc[(drop_i-1):]

        # must take into account history len;

        if self.backfill:
            self.backfill()

        super().__init__()


    def get_feature(self):
        #assert len(self.feature) > 0
        return self.feature

    def get_history_length(self):
        return self.history_lengh
    
    # -> override this ... 
    def compute(self, data_dict):
        return []

    def populate_feature(self):
        for index, value in self.get_TS().items():
            self.feature_numpy.append(value)
            self.feature[index] = value

    def update_feature(self, time, value):

        # we remove first item in dict, add the new one, FIFO style
        
        # maybe use hist length?
        if len(self.feature) > self.lookback:
            self.feature.popitem(last=False)

        self.feature[time] = value

        self.feature_numpy.append(value)

        # remove dis after you know this is indeed the case
        #assert len(self.feature) == self.history_lengh

    # backfill history
    def backfill(self):

        data = self.raw_data_manager.get_backfill_data()
        ff = self.compute(data)[-self.history_lengh:]
        
        #print(len(ff))
        #print(self.history_lengh)
        
        assert len(ff) == self.history_lengh

        self.feature_df[type(self).__name__] = ff

        self.populate_feature()

    # live update
    def update(self):
        data = self.raw_data_manager.get_live_data()

        new_val = self.compute(data)[-1]

        candle = self.raw_data_manager.get_live_candle()

        self.latest = new_val

        self.update_feature(candle.get('time'), new_val)


    def __getitem__(self, i):
        return self.feature[i]

    def __len__(self):
        return len(self.feature)

    def get_history_start_time(self):
        return self.feature_df.index[0]
    
    def get_DF(self):
        return self.feature_df

    def get_TS(self):
        return self.feature_df[type(self).__name__]

    def get_numpy(self):
        return self.feature_numpy

    def get_latest(self):
        return self.latest

    def get_lookback(self):
        return self.lookback

    def save_DF(self):
        name = type(self).__name__ + '.csv'
        self.feature_df.to_csv('data_test/features/' + name)
