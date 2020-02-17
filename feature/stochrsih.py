from feature.feature import EmptyFeature
import tulipy as ti


class StochRsiH(EmptyFeature):

    def __init__(self, p1, p2, p3, raw_data_manager, history_lengh=None):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        super().__init__(p1+p2+p3-2, raw_data_manager, name='_'.join([str(i) for i in [p1, p2, p3]]), history_lengh=history_lengh)

    def compute(self, data_dict):
        close = data_dict.get('close')
        high = data_dict.get('high')
        low = data_dict.get('low')

        return ti.stoch(high, low, close, 5, 3, 3)[0]
