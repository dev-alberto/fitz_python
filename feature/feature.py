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

        # raw data must be able to fill history
        assert (history_lengh + lookback - 1) <= raw_data_manager.get_history()
        assert lookback <= raw_data_manager.get_lookback()

        self.feature = RingBuffer(capacity=history_lengh, dtype=np.float64)

        # a feature may contain multiple features
        self.features = features


    def get_feature(self):
        assert len(self.feature) > 0
        return self.feature
    
    # -> override this ... 
    def compute(self, data_dict):
        return []

    # backfill history
    def backfill(self):
        data = self.raw_data_manager.get_backfill_data()
        ff = self.compute(data)[-self.history_lengh:]
        
        assert len(ff) == self.history_lengh

        for entry in ff:
            self.feature.append(entry)

    # live update
    def update(self):
        data = self.raw_data_manager.get_live_data()

        self.feature.append(self.compute(data)[-1:])
    
    def create_DF(self):
        pass
    
