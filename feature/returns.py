from feature.feature import EmptyFeature
import tulipy as ti
import numpy as np

class Returns(EmptyFeature):

    def __init__(self, history_lengh, raw_data_manager):
        super().__init__(history_lengh, 1, raw_data_manager)


    def compute(self, data_dict):
        
        close = data_dict.get('close')
        result = []
        for i in range(1, len(close)):
            result.append(close[i] - close[i-1])

        return np.array(result, dtype=object)