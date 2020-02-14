from feature.feature import EmptyFeature
import numpy as np


class High(EmptyFeature):

    def __init__(self, raw_data_manager, history_lengh=None):
        super().__init__(1, raw_data_manager, history_lengh=history_lengh)


    def compute(self, data_dict):
        
        high = data_dict.get('high')

        return np.array(high, dtype=object)
