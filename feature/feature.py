from numpy_ringbuffer import RingBuffer
import numpy as np
import pandas as pd

# should be an abstract class, all features will inherit from this.
# raw_data_manager contains the symbol, period data, so no need to add to constructor  
# there will probably be a "master" type class that supervises all features, saves to disk and 
# keeps a DF record
class EmptyFeature:
    
    def __init__(self, lookback, raw_data_manager, backfill=True, history_lengh=None, features=None):
        raw_data_length = raw_data_manager.get_history()

        # kind of spaghetii logic here to for feature history length but the gist is this:
        # one may specify history length when instantiating or we can produce the maximum length given the data available
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

        self.feature = RingBuffer(capacity=self.history_lengh, dtype=np.float64)
        self.latest = None

        # a feature may contain multiple features
        self.features = features

        self.feature_df = raw_data_manager.get_backfill_df()
        # trim df 
        drop_i = raw_data_length - self.history_lengh
        self.feature_df = self.feature_df.iloc[:-drop_i]
        #self.feature_df.drop(columns=['volume', 'low', 'high'],inplace=True)
        self.feature_df.set_index('time',inplace=True)

        if self.backfill:
            self.backfill()


    def get_feature(self):
        assert len(self.feature) > 0
        return self.feature

    def get_history_length(self):
        return self.history_lengh
    
    # -> override this ... 
    def compute(self, data_dict):
        return []

    # backfill history
    def backfill(self):
        data = self.raw_data_manager.get_backfill_data()
        ff = self.compute(data)[-self.history_lengh:]
        
        #print(len(ff))
        #print(self.history_lengh)
        
        assert len(ff) == self.history_lengh

        self.feature_df[type(self).__name__] = ff

        for entry in ff:
            self.feature.append(entry)

    # live update
    def update(self):
        data = self.raw_data_manager.get_live_data()

        new_val = self.compute(data)[-1]

        candle = self.raw_data_manager.get_live_candle()

        to_append = {'time': candle.get('time'), 'open': candle.get('open'), 'low':candle.get('low'), 'close':candle.get('close'),'high':candle.get('high'),'volume':candle.get('volume'),type(self).__name__:new_val}

        #print(to_append)
        #print(self.feature_df.head(5))
        
        self.latest = new_val

        self.feature.append(new_val)

        self.feature_df.append(pd.DataFrame(to_append,index=[to_append['time']]))
    
    # this should return a time indexed df containing feature values; maybe makes this a pandas series... 
    def get_DF(self):
        return self.feature_df

    def get_TS(self):
        return self.feature_df[type(self).__name__]

    def get_latest(self):
        return self.latest

    def save_DF(self):
        name = type(self).__name__ + '.csv'
        self.feature_df.to_csv('data_test/features/' + name)
