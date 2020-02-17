from feature.feature import EmptyFeature
import tulipy as ti


class Ema(EmptyFeature):
    def __init__(self, lookback, raw_data_manager, history_lengh=None):
        self.per = lookback
        super().__init__(lookback, raw_data_manager, name='_'+str(lookback), history_lengh=history_lengh)

    def compute(self, data_dict):
        close = data_dict.get('close')

        return ti.ema(close, self.per)
