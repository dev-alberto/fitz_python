from feature.feature import EmptyFeature
import tulipy as ti

import numpy as np


class LogReturns(EmptyFeature):

    def __init__(self, lookback, raw_data_manager, history_lengh=None):
        super().__init__(lookback, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        
        close = data_dict.get('close')

        open = data_dict.get('open')

        ret = np.log(close/open)

        return ti.sma(ret, self.lookback)
