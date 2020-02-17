from feature.feature import EmptyFeature
import tulipy as ti


class Adxr(EmptyFeature):

    def __init__(self, lookback, raw_data_manager, history_lengh=None):
        self.lookback = lookback

        super().__init__(lookback, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        close = data_dict.get('close')
        high = data_dict.get('high')
        low = data_dict.get('low')
        print("****")
        print(len(close))
        print(len(high))
        print(len(low))
        print(len(ti.adxr(high, low, close, 4)))
        print("****")
        return ti.adxr(high, low, close, self.lookback)
