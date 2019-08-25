from numpy_ringbuffer import RingBuffer
import numpy as np

# I would not add symbol, exchange here, not even period, 
# even tough they are clearly needed, I would to this one layer up..

# should be an abstract class, all features will inherit from this.
# raw_data_manager contains the symbol, period data, so no need to add to constructor  
# there will probably be a "master" type class that supervises all features, saves to disk and 
# keeps a DF record
class EmptyFeature:
    
    def __init__(self, history_lengh, lookback, raw_data_manager, features=None):
        self.history_lengh = history_lengh
        self.lookback = lookback
        self.raw_data_manager = raw_data_manager

        raw_data_length = raw_data_manager.get_history()

        # raw data must be able to fill history
        assert (history_lengh + lookback - 1) <= raw_data_length
        assert lookback <= raw_data_manager.get_lookback()

        self.feature = RingBuffer(capacity=history_lengh, dtype=np.float64)

        # a feature may contain multiple features
        self.features = features

        self.feature_df = raw_data_manager.get_backfill_df()
        # trim df in place
        drop_i = raw_data_length - history_lengh
        self.feature_df.drop(self.feature_df.index[:drop_i], inplace=True)
        self.feature_df.drop(columns=['volume', 'low', 'high'],inplace=True)
        self.feature_df.set_index('time',inplace=True)


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
        
        assert len(ff) == self.history_lengh

        self.feature_df[type(self).__name__] = ff

        for entry in ff:
            self.feature.append(entry)

    # live update
    def update(self):
        data = self.raw_data_manager.get_live_data()

        candle = self.raw_data_manager.get_live_candle()

        candle.pop('volume', None)
        candle.pop('low', None)
        candle.pop('high', None)

        new_val = self.compute(data)[-1:]

        candle[type(self).__name__] = new_val

        self.feature.append(new_val)

        self.feature_df.append(candle)
    
    # this should return a time indexed df containing feature values; maybe makes this a pandas series... 
    def get_DF(self):
        return self.feature_df

    def save_DF(self):
        name = type(self).__name__ + '.csv'
        self.feature_df.to_csv('data_test/features/' + name)