from feature.feature import EmptyFeature
import numpy as np


class Low(EmptyFeature):

    def __init__(self, raw_data_manager, history_lengh=None):
        super().__init__(1, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        
        low = data_dict.get('low')

        return np.array(low, dtype=object)
