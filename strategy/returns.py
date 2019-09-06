from strategy.strategy import AbstractStrategy
from feature.mean_returns import MeanReturns

import random


class Returns0(AbstractStrategy):

    def __init__(self,  raw_data_manager):
        #assert isinstance(mean_r, MeanReturns)
        super().__init__(initial_allocation=1, pair='BTCUSDT', period='1m', raw_data_managers=[raw_data_manager],
                         feature_list=[], model=None)

        self.raw_data_manager = raw_data_manager.get_backfill_df()


    def compute(self, ii):
        close = self.raw_data_manager["close"][ii]
        open = self.raw_data_manager["open"][ii]

        rr = (close - open) / close

        if rr > 0:
            self.allocation = 0

        else:
            self.allocation = 1

        return self.allocation

