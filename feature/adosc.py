from feature.feature import EmptyFeature
import tulipy as ti


class Adosc(EmptyFeature):

    def __init__(self, short_period, long_period, raw_data_manager, history_lengh=None):
        self.short_period = short_period
        self.long_period = long_period

        super().__init__(long_period, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        close = data_dict.get('close')
        volume = data_dict.get('volume')
        high = data_dict.get('high')
        low = data_dict.get('low')

        return ti.adosc(high, low, close, volume, self.short_period, self.long_period)
