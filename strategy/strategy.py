from raw_data_manager import RawDataManager
from ticker import Ticker
from strategy.alpha import Alpha
from feature.feature import EmptyFeature


from strategy.ITrade import ITradeAble
from strategy.backtest.IBacktest import IBacktestAble

from collections import OrderedDict
from collections.abc import Sequence
from datetime import datetime

import csv

# add book info, as well as other factors
class AbstractStrategy(Sequence, IBacktestAble, ITradeAble):

    def __init__(self, raw_data_manager, alphas, features=[], ticker=None, init_alloc=0):

        assert isinstance(raw_data_manager, RawDataManager)
        
        if ticker is not None:    
            assert isinstance(ticker, Ticker)

        assert isinstance(alphas, dict)
        
        self.raw_data_manager = raw_data_manager

        self.alphas = alphas

        self.ticker = ticker
        
        self.features = features

        self.start_time = self.get_earliest_start_time()

        self.history = min([a.get_history_len() for a in self.alphas.keys()])

        self.strategy = OrderedDict()
        self.strategy[self.start_time] = init_alloc

        self.csv_path = 'data_test/live/strategies/' + type(self).__name__ + '.csv'
        alpha_names = [type(list(alphas.keys())[i]).__name__ for i in range(len(alphas))]
        
        strategy_file = open(self.csv_path, 'w+')
            
        r1 = raw_data_manager.get_latest()

        for k in alpha_names:
            r1[k] = init_alloc
        r1['strategy'] = 0
        r1['bid'] = 0
        r1['ask'] = 0
        #r1['ticker_time'] = 0
        self.fieldnames = list(r1.keys())
        writer = csv.DictWriter(strategy_file, fieldnames=self.fieldnames)

        writer.writeheader()
        writer.writerow(r1)

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

        #print(ii)
        log = {}
        log['bid'] = self.ticker.get_bid()
        log['ask'] = self.ticker.get_ask()
        #log['ticker_time'] = datetime.fromtimestamp(self.ticker.get_time())

        position = 0
        for a, w in self.alphas.items():
            alloc = a.compute(ii)
            position += alloc * w
            log[type(a).__name__] = alloc

        if len(self.strategy) > self.history:
            self.strategy.popitem(last=False)
        
        self.strategy[ii] = position

        log['strategy'] = position

        llog = {**log, **self.raw_data_manager.get_latest()}
        
        strategy_file = open(self.csv_path, 'a')

        writer = csv.DictWriter(strategy_file, fieldnames=self.fieldnames)
        writer.writerow(llog)

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
