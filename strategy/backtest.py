import pandas as pd

class Backtest:

    def __init__(self, raw_data_manager, strategy, cost):
        self.strategy = strategy
        self.cost = cost
        # self.initial_allocation = initial_allocation
        self.raw_data_manager = raw_data_manager
    
    def compute_pnl(self):
        data = self.raw_data_manager.get_backfill_df()
        start_position = self.strategy.get_current()
    
        data = data[(data['time'] >= start_position['ts'])]


        data.index = pd.RangeIndex(len(data.index))
        print(data.head(5))
        print(data.loc[0, 'close'])

        returns = []

        for index, row in data.iterrows():
            position = self.strategy.compute()
            alloc = position['allocation']            
            if len(returns) == 0:
                returns.append(0)
                continue
            val = alloc * (row['close'] - data.loc[index-1, 'close'])
            returns.append(val)

        
        #data['portfolio'] = portfolio
        data['returns'] = returns

        return data

            

    def compute_cumulative_pnl(self):
        pass
    

    def compute_range_pnl(self):
        pass
