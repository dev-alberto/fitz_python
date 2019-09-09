from raw_data_manager import RawDataManager
from strategy.ITrade import ITradeAble
from strategy.backtest.IBacktest import IBacktestAble

from collections import OrderedDict
from collections.abc import Sequence

class Alpha(Sequence, IBacktestAble, ITradeAble):

    def __init__(self, pair, period, raw_data_managers, 
    feature_list=None, model=None, init_alloc=0, history=10000):
        
        self.pair = pair
        self.period = period
        self.model = model
        self.feature_list = feature_list

        self.history = history

        assert len(raw_data_managers) > 0

        self.raw_data_managers = raw_data_managers

        self.main_data_manager = None
        
        for m in raw_data_managers:
            assert isinstance(m, RawDataManager)
            # exchange should also be here
            if period == m.get_period() and pair == m.get_symbol():
                self.main_data_manager = m
                break
        
        assert self.main_data_manager is not None
        
        self.allocation = init_alloc

        self.start_time = self.get_earliest_start_time()

        self.alpha = OrderedDict()
        self.alpha[self.start_time] = init_alloc



    def backfill(self, time_index):
        for ii in time_index:
            self.alpha[ii] =  self.compute(ii)

        return self.alpha

    def generate_position(self, ii):
        self.update_features()
        
        position = self.compute(ii)

        if len(self.alpha) > self.history:
            self.alpha.popitem(last=False)
        
        self.alpha[ii] = position

        return position

    def compute(self, ii):
        return self.allocation

    def update_features(self):
        if self.feature_list is not None:
            for f in self.feature_list:
                f.update()

    def get_earliest_start_time(self):
        if len(self.feature_list) == 0:
            return self.main_data_manager.get_backfill_data()['time'][0]
    
        dates = []
        for f in self.feature_list:
            dd =  f.get_history_start_time()
            # print(dd.index)
            dates.append(dd)
        
        return max(dates)

    def get_main_data_manager(self):
        return self.main_data_manager

    def get_features(self):
        return self.feature_list

    def get_history_len(self):
        return self.history

    def __eq__(self, other_alpha):
        return isinstance(other_alpha, Alpha) and type(self).__name__ == type(other_alpha).__name__

    def __hash__(self):
        return hash(str(self))

    def __getitem__(self, i):
        return self.alpha[i]

    def __len__(self):
        return len(self.alpha)