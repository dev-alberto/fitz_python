from strategy.strategy import AbstractStrategy
import random

class RandomBTCUSDT(AbstractStrategy):

    def __init__(self, raw_data_manager):
        super().__init__(initial_allocation=1, pair='BTCUSDT', period='1m', raw_data_managers=[raw_data_manager], feature_list=None, model=None)

    def compute(self, ii):

        predict = random.uniform(0,1)

        if predict > 0.5:
            self.allocation =  random.uniform(0,1)
        
        return self.allocation
