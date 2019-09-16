from strategy.alpha import Alpha
#from feature.LogReturns import LogReturns

import random


class Returns0(Alpha):

    def __init__(self, log_returns, raw_data_manager):
        self.log_returns = log_returns
       # assert isinstance(log_returns, LogReturns)

        super().__init__('BTCUSDT','1m',[raw_data_manager],feature_list=[log_returns])

    def compute(self, ii):

        lr = self.log_returns[ii]

        if lr > 0:
            self.allocation = 1

        else:
            self.allocation = 1

        return self.allocation

