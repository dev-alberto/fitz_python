from feature.feature import EmptyFeature
from feature.bollinger_high import BollingerHigh
import tulipy as ti

class Cross_cBH(EmptyFeature):

    def __init__(self, bollingerH, raw_data_manager, history_l=None):
        
        assert isinstance(bollingerH, BollingerHigh)
        self.boll = bollingerH

        super().__init__(2, raw_data_manager, features=[bollingerH])

    def compute(self, data_dict):

        close = data_dict['close']
        f1 = self.boll.get_numpy()

        return ti.crossover(close, f1)
