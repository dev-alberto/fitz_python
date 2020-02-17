from feature.feature import EmptyFeature
import tulipy as ti


class Atr(EmptyFeature):

    def __init__(self, lookback, raw_data_manager, history_lengh=None):
        self.per = lookback

        super().__init__(lookback, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        high = data_dict.get('high')
        low = data_dict.get('low')
        close = data_dict.get('close')

        return ti.atr(high, low, close, self.per)
