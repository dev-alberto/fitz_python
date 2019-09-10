from feature.feature import EmptyFeature
import numpy as np

class Open(EmptyFeature):

    def __init__(self,raw_data_manager, history_lengh=None):
        super().__init__(2, raw_data_manager, history_lengh=history_lengh)


    def compute(self, data_dict):
        
        open_ = data_dict.get('open')

        return np.array(open_, dtype=object)
