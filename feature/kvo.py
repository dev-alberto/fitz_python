from feature.feature import EmptyFeature
import tulipy as ti


class Kvo(EmptyFeature):

    def __init__(self, short_period, long_period, raw_data_manager, history_lengh=None):
        self.short_period = short_period
        self.long_period = long_period

        super().__init__(long_period - 1, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        high = data_dict.get('high')
        low = data_dict.get('low')
        close = data_dict.get('close')
        volume = data_dict.get('volume')

        return ti.kvo(high, low, close, volume, self.short_period, self.long_period)
