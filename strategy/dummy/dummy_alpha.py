from strategy.alpha import Alpha
from feature.close import Close


class DumbAlpha(Alpha):

    def __init__(self, close5, close1, open1, high1, low1, raw_data_manager):
        self.close5 = close5
        self.close1 = close1
        self.high1 = high1
        self.low1 = low1
        self.open1 = open1
        super().__init__('BTCUSDT', '1m', [raw_data_manager], feature_list=[close5, close1, open1, high1, low1])
        self.my_change = 0

    def compute(self, ii):

        # print('last close %s' % self.close1[ii])

        # print(self.close5.get_feature())

        #a = self.close5[ii] - self.close5[ii-1]

        formula = (self.close1.get_latest().get('value') - self.open1.get_latest().get('value'))# / (self.high1.get_latest().get('value') - self.low1.get_latest().get('value'))
        if formula > 0:
            valret = 1
        else:
            valret=-1


        #print(self.cumulative_pnl)
        self.my_change = self.allocation - valret

        self.allocation = valret


        return self.allocation


