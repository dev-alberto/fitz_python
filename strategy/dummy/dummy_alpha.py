from strategy.alpha import Alpha
from feature.close import Close


class DumbAlpha(Alpha):

    def __init__(self, close1, close5, raw_data_manager):
        self.close1 = close1
        self.close5 = close5

        super().__init__('BTCUSDT', '1m', [raw_data_manager], feature_list=[close1, close5])

    def compute(self, ii):

        # print('last close %s' % self.close1[ii])

        # print(self.close5.get_feature())

        self.allocation = 1

        return self.allocation


