from strategy.strategy import AbstractStrategy
import random

class RandomBTCUSDT(AbstractStrategy):

    def __init__(self, raw_data_manager):
        super().__init__(pair='BTCUSDT', period='1m', lookback=256, feature_list=None, model=None, raw_data_managers=[raw_data_manager])
        
        self.time_data = raw_data_manager.get_backfill_data().get('time')

        # start the strategy at the lookback index
        self.index = self.lookback
        # prediction format 
        self.current_prediction = {'allocation':0, 'ts':self.time_data[self.index]}

    def compute(self):

        predict = random.uniform(0,1)

        if predict > 0.5:
            self.current_prediction = {'allocation':random.uniform(0,1), 'ts':self.time_data[self.index]}
            self.index = self.index + 1
            return self.current_prediction
        
        self.current_prediction['ts'] = self.time_data[self.index]
        self.index = self.index + 1
        return self.current_prediction
