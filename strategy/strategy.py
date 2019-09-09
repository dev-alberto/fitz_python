from raw_data_manager import RawDataManager
from ticker import Ticker
from strategy.alpha import Alpha
from feature.feature import EmptyFeature

from strategy.ITrade import ITradeAble
from strategy.backtest.IBacktest import IBacktestAble

from collections import OrderedDict
from collections.abc import Sequence

# add book info, as well as other factors
class AbstractStrategy(Sequence, IBacktestAble, ITradeAble):

    def __init__(self, raw_data_manager, alphas, ticker=None, init_alloc=0):

        assert isinstance(raw_data_manager, RawDataManager)
        
        if ticker is not None:    
            assert isinstance(ticker, Ticker)

        assert isinstance(alphas, dict)
        
        self.raw_data_manager = raw_data_manager

        self.alphas = alphas

        self.ticker = ticker
        
        self.features = []

        for alpha in alphas.keys():
            assert isinstance(alpha, Alpha)
            ff = alpha.get_features()
            if ff is not None:
                for f in ff:
                    assert isinstance(f, EmptyFeature)
                    self.features.append(f)

        self.start_time = self.get_earliest_start_time()

        self.history = min([a.get_history_len() for a in self.alphas.keys()])

        self.strategy = OrderedDict()
        self.strategy[self.start_time] = init_alloc

    # for backtest purpose only
    def backfill(self, time_index):

        # backfill alphas
        for k in self.alphas.keys():
            k.backfill(time_index)

        for index in time_index:
            position = 0
            
            for a, w in self.alphas.items():
                alloc = a[index]
                position += alloc * w

            self.strategy[index] = position

        return self.strategy


    def generate_position(self, ii):
        self.update_features()

        print('Generating position... at')
        print(ii)
        print('Ticker 1 ... ')
        print(self.ticker.get_bid())

        position = 0
        for a, w in self.alphas.items():
            alloc = a.compute(ii)
            position += alloc * w

        if len(self.strategy) > self.history:
            self.strategy.popitem(last=False)
        
        self.strategy[ii] = position
        
        print('Position generated, ticker is ... ')
        print(self.ticker.get_bid())

        return position


    def update_features(self):
        for f in self.features:
            f.update()


    def get_earliest_start_time(self):
        dates = []
        for alpha in self.alphas.keys():
            dd = alpha.get_earliest_start_time()
            dates.append(dd)
        
        return max(dates)

    def get_main_data_manager(self):
        return self.raw_data_manager


    def __eq__(self, other_strategy):
        return isinstance(other_strategy, AbstractStrategy) and type(self).__name__ == type(other_strategy).__name__

    def __hash__(self):
        return hash(str(self))

    def __getitem__(self, i):
        return self.strategy[i]

    def __len__(self):
        return len(self.strategy)
