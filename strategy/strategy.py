# 
class AbstractStrategy:

    def __init__(self, pair, period, lookback, feature_list=None, model=None, raw_data_managers=None):
        self.pair = pair
        self.period = period
        self.lookback = lookback
        self.model = model
        self.feature_list = feature_list
        self.raw_data_managers = raw_data_managers

        
        self.current_prediction = None
    
    def compute(self):
        return {}
    
    def get_lookback(self):
        return self.lookback

    def get_current(self):
        return self.current_prediction 