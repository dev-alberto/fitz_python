from feature.feature import EmptyFeature
import tulipy as ti


class Mfi(EmptyFeature):

    def __init__(self, lookback, raw_data_manager, history_lengh=None):
        self.per = lookback

        super().__init__(lookback+1, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        close = data_dict.get('close')
        volume = data_dict.get('volume')
        high = data_dict.get('high')
        low = data_dict.get('low')

        return ti.mfi(high, low, close, volume, self.per)
