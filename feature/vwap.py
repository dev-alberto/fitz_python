from feature.feature import EmptyFeature
import tulipy as ti


class Vwap(EmptyFeature):

    def __init__(self, lookback, raw_data_manager, history_lengh=None):
        self.per = lookback
        super().__init__(lookback, raw_data_manager,history_lengh=history_lengh)

    def compute(self, data_dict):
        close = data_dict.get('close')
        volume = data_dict.get('volume')
        
        return ti.vwma(close, volume, self.per)
