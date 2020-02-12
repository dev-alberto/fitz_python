from feature.feature import EmptyFeature
from feature.bollinger_middle import BollingerMiddle
import tulipy as ti

class Cross_BMc(EmptyFeature):

    def __init__(self, bollingerM, raw_data_manager, history_l=None):

        assert isinstance(bollingerM, BollingerMiddle)
        self.boll = bollingerM
        super().__init__(2, raw_data_manager, features=[bollingerM])

    def compute(self, data_dict):

        close = data_dict['close']

        f1 = self.boll.get_numpy()

        return ti.crossover(f1, close)
