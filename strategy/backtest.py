import pandas as pd
from data_retriever import Parse_string_date
from strategy.strategy import AbstractStrategy
from feature.feature import EmptyFeature
import matplotlib.pyplot as plt

# stats need to be added 
class Backtest:

    def __init__(self, strategy, cost,start_time=None):
        assert isinstance(strategy, AbstractStrategy)

        self.strategy = strategy
        self.cost = cost
        
        strategy_min_time = strategy.get_earliest_start_time()

        if start_time is not None: 
            self.start_time = Parse_string_date(start_time)
            if strategy_min_time > self.start_time:
                self.start_time = strategy_min_time
        else:
            self.start_time = strategy_min_time

    def compute_pnl(self, save=True):
         
        data = self.strategy.get_main_data_manager().get_backfill_df()
    
        data = data[(data['time'] >= self.start_time)]

        assert (len(data)) > 0

        data.set_index('time',inplace=True)

        returns = []

        allocs = []

        for index, row in data.iterrows():
            alloc = self.strategy.compute(index)

            allocs.append(alloc)

            cost = (self.cost/100.0) * alloc * row['open']

            val = alloc * (row['close'] - row['open']) - cost
            
            returns.append(val)

        
        #data['portfolio'] = portfolio
        data['returns'] = returns
        data['allocs'] = allocs
        return data

    def plot_pnl(self, period='60T'):
        ll = self.compute_pnl()

        ret = pd.Series(data = ll['returns'], index = ll.index)

        hh = ret.resample(period).sum()

        cum = hh.cumsum()

        cum.plot()

        plt.show()

    def save_to_disk(self, path='data_test/backtest/'):
        df = self.compute_pnl()
        name = type(self.strategy).__name__ + '.csv'
        df.to_csv(path + name)

    def compute_cumulative_pnl(self):
        pass
    

    def compute_range_pnl(self):
        pass
