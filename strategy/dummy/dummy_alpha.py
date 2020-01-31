from strategy.alpha import Alpha
from feature.close import Close
import random


class DumbAlpha(Alpha):

    def __init__(self, cls1min, open1min, close5, close1, open1, high1, low1, open5, close15, open15, close30, open30,
                 raw_data_manager):
        self.cls1min = cls1min
        self.open1min = open1min
        self.close5 = close5
        self.close1 = close1
        self.high1 = high1
        self.low1 = low1
        self.open1 = open1
        self.open5 = open5
        self.open15 = open15
        self.close15 = close15
        self.open30 = open30
        self.close30  = close30
        self.rounded_indicies = []
        super().__init__('BTCUSDT', '1m', [raw_data_manager], feature_list=[cls1min, open1min, close5, close1, open1, high1, low1, open5, close15, open15, close30, open30])

    def compute(self, ii):

        # print('last close %s' % self.close1[ii])

        # print(self.close5.get_feature())

        #a = self.close5[ii] - self.close5[ii-1]

        #formula = (self.close1.get_latest().get('value') - self.open1.get_latest().get('value'))# / (self.high1.get_latest().get('value') - self.low1.get_latest().get('value'))

        #print(ii)

        #formula = self.cls1min[ii] - self.open1min[ii]
        formula = self.close5[ii] - self.open5[ii]

        #formula = self.close5[ii] - self.open5[ii]

        #print("*****")
        #print(self.close1.get_feature())

        #if formula > 0:
        #    valret = 1
        #else:
        #    valret = -1

        if formula == 0:
            self.allocation = 0
        else:
            self.allocation = formula

        self.allocation=formula
        #predict = random.uniform(0, 1)
        # print(self.change_position_pnl)

        #if predict > 0.7:
         #   self.allocation = 0

        return self.allocation

    def fill_rounded(self, dates):
        for ii in dates:
            self.rounded_indicies.append(self.close5.get_rounded_index(ii))

    def run_data_tests(self):
        print("Running tests .... ")
        for i in range(len(self.rounded_indicies)-4):
            print("*****")
            for j in range(5):
                print(self.rounded_indicies[i+j])
                assert self.rounded_indicies[i] == self.rounded_indicies[i+j]


