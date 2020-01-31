import pandas as pd
from data_retriever import Parse_string_date
from strategy.backtest.IBacktest import IBacktestAble

import matplotlib.pyplot as plt


# stats need to be added; needs to work with alpha/strategy; create extra level of abstraction
class Simulator:

    def __init__(self, backtestAble, cost, start_time=None):
        assert isinstance(backtestAble, IBacktestAble)

        self.backtestAble = backtestAble
        self.cost = cost
        
        min_time = backtestAble.get_earliest_start_time()

        if start_time is not None: 
            self.start_time = Parse_string_date(start_time)
            if min_time > self.start_time:
                self.start_time = min_time
        else:
            self.start_time = min_time

        self.end_time = self.backtestAble.get_last_time_index()

        self.DF = self.compute_pnl()

    def compute_pnl(self):
         
        data = self.backtestAble.get_main_data_manager().get_backfill_df_between(self.start_time, self.end_time)

        # fiecare feature va da last time, ca sa stim unde sa taiem simularea
        self.backtestAble.backfill(data.index)

        returns = []

        allocs = []
        
        prev_alloc = 0
        prevprev_alloc = 0

        for i in range(0, len(data)-1):

            index = data.index[i]
            next_index = data.index[i+1]

            alloc = self.backtestAble[index]

            allocs.append(alloc)
            # prev alloc
            cost = (self.cost/100.0) * abs(alloc - prev_alloc) * data.loc[index, "open"]

            val = alloc * (data.loc[next_index, "close"] - data.loc[next_index, "open"]) # - cost

            prev_alloc = alloc
            returns.append(val)

        # for i in range(0, 200-4):
        #
        #     index = data.index[i]
        #     next_index = data.index[i+4]
        #
        #     alloc = self.backtestAble[next_index]
        #
        #     allocs.append(alloc)
        #     ret = (data.loc[next_index, "close"] - data.loc[next_index, "open"])
        #     val = alloc * (data.loc[next_index, "close"] - data.loc[next_index, "open"]) # - cost
        #     print("*****")
        #     print("alloc   %s", alloc )
        #     print("returns   %s", ret)
        #     returns.append(val)
        #

        # for i in range(4):
        #     returns.append(0)
        #     allocs.append(0)
        #
        #
        data['returns'] = returns

        # data['allocs'] = allocs
        #
        # return data

    def plot_pnl(self, period='60T'):

        ret = pd.Series(data=self.DF['returns'], index=self.DF.index)

        # hh = ret.resample(period).sum()

        #cum = hh.cumsum()
        cum = ret.cumsum()
        cum.plot()

        plt.show()

    def save_to_disk(self, path='data_test/backtest/'):
        name = type(self.backtestAble).__name__ + '.csv'
        self.DF.to_csv(path + name)

    def compute_cumulative_pnl(self):
        pass

    def compute_range_pnl(self):
        pass
