from feature.feature import EmptyFeature
import tulipy as ti

class Vwap(EmptyFeature):

    def __init__(self, history_lengh, lookback, raw_data_manager):
        super().__init__(history_lengh, lookback, raw_data_manager)


    def compute(self, data_dict):
        close = data_dict.get('close')
        volume = data_dict.get('volume')
        
        return ti.vwma(close, volume, self.lookback)