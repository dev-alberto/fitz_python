from feature.feature import EmptyFeature
from feature.bollinger_low import BollingerLow
import tulipy as ti

class Cross_cBL(EmptyFeature):

    def __init__(self, bollingerL, raw_data_manager,history_l=None):
        assert isinstance(bollingerL, BollingerLow)
        self.boll = bollingerL
        super().__init__(2, raw_data_manager, features=[bollingerL])

    def compute(self, data_dict):

        close = data_dict['close']
        f1 = self.boll.get_feature()

        return ti.crossover(close, f1)
