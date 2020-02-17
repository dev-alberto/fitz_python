from feature.feature import EmptyFeature
import tulipy as ti


class Pvi(EmptyFeature):

    def __init__(self, raw_data_manager, history_lengh=None):
        super().__init__(1, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        close = data_dict.get('close')
        volume = data_dict.get('volume')

        return ti.pvi(close, volume)
