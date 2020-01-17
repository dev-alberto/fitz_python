from strategy.alpha import Alpha
from feature.close import Close
import random


class DumbAlpha(Alpha):

    def __init__(self, cls1min, open1min, close5, close1, open1, high1, low1, open5, raw_data_manager):
        self.cls1min = cls1min
        self.open1min = open1min
        self.close5 = close5
        self.close1 = close1
        self.high1 = high1
        self.low1 = low1
        self.open1 = open1
        self.open5  = open5
        super().__init__('BTCUSDT', '1m', [raw_data_manager], feature_list=[cls1min, open1min, close5, close1, open1, high1, low1, open5])

    def compute(self, ii):

        # print('last close %s' % self.close1[ii])

        # print(self.close5.get_feature())

        #a = self.close5[ii] - self.close5[ii-1]

        #formula = (self.close1.get_latest().get('value') - self.open1.get_latest().get('value'))# / (self.high1.get_latest().get('value') - self.low1.get_latest().get('value'))

        #print(ii)

        #formula = (self.cls1min[ii] - self.open1min[ii])
        #formula = self.close1[ii] - self.open1[ii]

        formula = self.close5[ii] #- self.open5[ii]

        #print("*****")
        #print(self.close1.get_feature())

        #if formula > 0:
        #    valret = 1
        #else:
        #    valret = -1

        if formula == 0:
            self.allocation = 0
        else:
            self.allocation = 1 / formula


        #predict = random.uniform(0, 1)
        # print(self.change_position_pnl)

        #if predict > 0.7:
         #   self.allocation = 0

        return self.allocation


