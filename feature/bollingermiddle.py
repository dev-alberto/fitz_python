from feature.feature import EmptyFeature
import tulipy as ti


class BollingerMiddle(EmptyFeature):

    def __init__(self, lookback, std,  raw_data_manager, history_lengh=None):
        self.per = lookback
        self.std = std

        super().__init__(lookback, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        
        close = data_dict.get('close')

        return ti.bbands(close, self.per, self.std)[1]
