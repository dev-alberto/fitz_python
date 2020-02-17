from feature.feature import EmptyFeature
import tulipy as ti


class Cvi(EmptyFeature):

    def __init__(self, lookback, raw_data_manager, history_lengh=None):
        self.per = lookback

        super().__init__(2*lookback, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        high = data_dict.get('high')
        low = data_dict.get('low')

        return ti.cvi(high, low, self.per)
