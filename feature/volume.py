from feature.feature import EmptyFeature
import numpy as np


class Volume(EmptyFeature):

    def __init__(self, raw_data_manager, history_lengh=None):
        super().__init__(2, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        
        volume = data_dict.get('volume')

        return np.array(volume, dtype=object)
