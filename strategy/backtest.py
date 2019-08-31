import pandas as pd
from data_retriever import Parse_string_date
from strategy.strategy import AbstractStrategy
from feature.feature import EmptyFeature

class Backtest:

    def __init__(self, start_time, strategy, cost):
        assert isinstance(strategy, AbstractStrategy)

        self.strategy = strategy
        self.cost = cost
        self.start_time = Parse_string_date(start_time)

        strategy_min_time = strategy.get_earliest_start_time()
        if strategy_min_time > self.start_time:
            self.start_time = strategy_min_time

    def compute_pnl(self, save=True):
         
        data = self.strategy.get_main_data_manager().get_backfill_df()
    
        data = data[(data['time'] >= self.start_time)]

        assert (len(data)) > 0

        data.set_index('time',inplace=True)

        #data.index = pd.RangeIndex(len(data.index))
        #print(data.head(5))
        #print(data.loc[0, 'close'])

        returns = []

        allocs = []

        prev = None

        for index, row in data.iterrows():
            alloc = self.strategy.compute(index)
            allocs.append(alloc)
            if len(returns) == 0:
                returns.append(0)
                prev = row['close']
                continue
            val = alloc * (row['close'] - prev)
            returns.append(val)

            prev = row['close']

        
        #data['portfolio'] = portfolio
        data['returns'] = returns
        data['allocs'] = allocs
        return data

    def compute_cumulative_pnl(self):
        pass
    

    def compute_range_pnl(self):
        pass
