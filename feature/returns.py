from feature.feature import EmptyFeature
import numpy as np


class Returns(EmptyFeature):

    def __init__(self, raw_data_manager, history_lengh=None):
        super().__init__(2, raw_data_manager, history_lengh=history_lengh)

    def compute(self, data_dict):
        
        close = data_dict.get('close')
        result = [0]
        for i in range(1, len(close)):
            result.append(close[i] - close[i-1])

        return np.array(result, dtype=object)
