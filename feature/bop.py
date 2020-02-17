from feature.feature import EmptyFeature
import tulipy as ti


class Bop(EmptyFeature):

    def __init__(self, raw_data_manager, history_lengh=None):

        super().__init__(1, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        high = data_dict.get('high')
        low = data_dict.get('low')
        close = data_dict.get('close')
        open_ = data_dict.get('open')

        return ti.bop(open_,high, low, close)
