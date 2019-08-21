class AbstractModel:

    def __init__(self, pair, lookback, feature_list=None, raw_data_managers=None):
        self.pair = pair
        self.lookback = lookback
        self.feature_list = feature_list
        self.raw_data_managers = raw_data_managers

        self.model = None

    def train(self):
        pass

    def save_model(self):
        pass

    def get_model(self):
        return self.model
