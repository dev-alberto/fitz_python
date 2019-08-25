from strategy.strategy import AbstractStrategy
from feature.mean_returns import MeanReturns

import random

class Min_Max_Normalized_Returns_Reversion(AbstractStrategy):

    def __init__(self, mean_r, raw_data_manager):
        assert isinstance(mean_r, MeanReturns)
        super().__init__(initial_allocation=1, pair='BTCUSDT', period='1m', raw_data_managers=[raw_data_manager], feature_list=[mean_r], model=None)

        self.mean_r_feature = mean_r.get_DF()

        self.min = self.mean_r_feature['MeanReturns'].min()
        self.max = self.mean_r_feature['MeanReturns'].max()

        #print(self.min)

        #print(self.max)

    def compute(self, ii):
        
        val = self.mean_r_feature.loc[ii, 'MeanReturns']

        if val > self.max:
            self.max = val
        
        if val < self.min:
            self.min = val

        normalized = (val - self.min) / (self.max - self.min)

        self.allocation = - normalized

        return self.allocation
