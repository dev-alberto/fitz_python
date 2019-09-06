from ticker import Ticker
from raw_data_manager import RawDataManager
from strategy.strategy import AbstractStrategy

from feature.feature import EmptyFeature

class AbstractLiveStrategy:

    def __init__(self, size, raw_data_manager, ticker, strategies, features):

        assert isinstance(raw_data_manager, RawDataManager)
        assert isinstance(ticker, Ticker)
        assert isinstance(strategies, list)
        for s in strategies:
            assert isinstance(s, AbstractStrategy)

        for f in features:
            assert isinstance(f, EmptyFeature)
        
        self.size = size 
        self.raw_data_manager = raw_data_manager
        self.strategies = strategies
        self.features = features
        self.ticker = ticker

        self.strategy_weights = {}

        # assign 0 weights at start
        for s in strategies:
            self.strategy_weights[s] = 0
        

    def generate_position(self, ii):
        self.update_features()
        
        position = 0
        for s, w in self.strategy_weights.items():
            alloc = s.compute(ii)
            position += alloc * w

        return position


    # override dis
    def assign_weights(self):
        return self.strategy_weights

    def update_features(self):
        for f in self.features:
            f.update()
