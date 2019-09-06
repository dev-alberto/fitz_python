from strategy.strategy import AbstractStrategy
from feature.LogReturns import LogReturns

import random


class Returns0(AbstractStrategy):

    def __init__(self, log_returns, raw_data_manager):
        assert isinstance(log_returns, LogReturns)
        super().__init__(initial_allocation=1, pair='BTCUSDT', period='1m', raw_data_managers=[raw_data_manager],
                         feature_list=[log_returns], model=None)

        self.log_returns = log_returns.get_TS()


    def compute(self, ii):

        lr = self.log_returns[ii]

        if lr > 0:
            self.allocation = 1

        else:
            self.allocation = 1

        return self.allocation

