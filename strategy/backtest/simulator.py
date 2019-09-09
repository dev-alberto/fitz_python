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

        self.DF = self.compute_pnl()

    def compute_pnl(self):
         
        data = self.backtestAble.get_main_data_manager().get_backfill_df_from(self.start_time)

        self.backtestAble.backfill(data.index)

        returns = []

        allocs = []
        
        prev_alloc = 0
        prevprev_alloc = 0

        for index, row in data.iterrows():

            alloc = self.backtestAble[index]

            allocs.append(alloc)

            # prev alloc
            cost = (self.cost/100.0) * abs(prev_alloc - prevprev_alloc) * row['open']

            val = prev_alloc * (row['close'] - row['open'])  - cost

            prevprev_alloc = prev_alloc
            prev_alloc = alloc
            
            returns.append(val)

        
        data['returns'] = returns
        data['allocs'] = allocs

        return data

    def plot_pnl(self, period='60T'):

        ret = pd.Series(data = self.DF['returns'], index = self.DF.index)

        hh = ret.resample(period).sum()

        cum = hh.cumsum()

        cum.plot()

        plt.show()

    def save_to_disk(self, path='data_test/backtest/'):
        name = type(self.backtestAble).__name__ + '.csv'
        self.DF.to_csv(path + name)

    def compute_cumulative_pnl(self):
        pass
    

    def compute_range_pnl(self):
        pass
