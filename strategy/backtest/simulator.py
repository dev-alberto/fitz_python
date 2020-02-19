import pandas as pd
from data.data_retriever import Parse_string_date
from strategy.backtest.IBacktest import IBacktestAble
from data.raw_data_manager import RawDataManager

import matplotlib.pyplot as plt


# stats need to be added; needs to work with alpha/strategy; create extra level of abstraction
class Simulator:

    def __init__(self, backtestAble, raw_data_manager, cost, start_time=None):

        assert isinstance(backtestAble, IBacktestAble)
        assert isinstance(raw_data_manager, RawDataManager)

        self.backtestAble = backtestAble
        self.cost = cost
        self.raw_data_manager = raw_data_manager

        min_time = backtestAble.get_earliest_start_time()

        if start_time is not None: 
            self.start_time = Parse_string_date(start_time)
            if min_time > self.start_time:
                self.start_time = min_time
        else:
            self.start_time = min_time

        self.end_time = self.backtestAble.get_last_time_index()

        self.returns = {}

    def compute_pnl(self):
         
        data = self.raw_data_manager.get_backfill_df_between(self.start_time, self.end_time)

        print('Start time %s ', self.start_time)
        print('End time %s ', self.end_time)

        # fiecare feature va da last time, ca sa stim unde sa taiem simularea
        self.backtestAble.backfill(data.index)

        for i in range(0, len(data)-1):

            index = data.index[i]
            next_index = data.index[i+1]

            if i == 0:
                self.returns[index] = 0
                continue

            alloc = self.backtestAble[index]

            ret = (data.loc[next_index, "close"] - data.loc[index, "close"])
            val = alloc * ret #(data.loc[next_index, "close"] - data.loc[next_index, "open"]) # - cost

            self.returns[index] = val

        return self.returns

    def plot_pnl(self, period='60T'):

        ret_d = self.compute_pnl()
        ret = pd.Series(ret_d)
        # hh = ret.resample(period).sum()

        # cum = hh.cumsum()
        cum = ret.cumsum()
        cum.plot()

        plt.show()

    def save_to_disk(self, path='data_test/backtest/'):
        name = type(self.backtestAble).__name__ + '.csv'
        # self.DF.to_csv(path + name)

    def compute_cumulative_pnl(self):
        pass

    def compute_range_pnl(self):
        pass
