from feature.feature import EmptyFeature
from feature.bollingermiddle import BollingerMiddle
import tulipy as ti


class CrossCbm(EmptyFeature):

    def __init__(self, bollingerM, raw_data_manager, history_l=None):
        assert isinstance(bollingerM, BollingerMiddle)
        self.boll = bollingerM
        super().__init__(2, raw_data_manager, features=[bollingerM])

    def compute(self, data_dict):

        close = data_dict['close']

        f1 = self.boll.get_numpy()

        return ti.crossover(close, f1)
