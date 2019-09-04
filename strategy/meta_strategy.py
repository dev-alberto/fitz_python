from ticker import Ticker
from raw_data_manager import RawDataManager
from strategy.strategy import AbstractStrategy


class AbstractMeta:

    def __init__(self, size, raw_data_manager, ticker, strategies):

        assert isinstance(raw_data_manager, RawDataManager)
        assert isinstance(ticker, Ticker)
        assert isinstance(strategies, list)
        for s in strategies:
            assert isinstance(s, AbstractStrategy)
        
        self.size = size 
        self.raw_data_manager = raw_data_manager
        self.strategies = strategies
        self.ticker = ticker

        self.strategy_weights = {}

        # assign 0 weights at start
        for s in strategies:
            self.strategy_weights[s] = 0
        

    def generate_position(self, ii):
        position = 0
        for s, w in self.strategy_weights.items():
            alloc = s.compute(ii)
            position += alloc * w

        return position


    # override dis
    def assign_weights(self):
        return self.strategy_weights
