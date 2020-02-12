from strategy.alpha import Alpha
import random


class BollingerImpl2(Alpha):

    def __init__(self, log_returns, bollinger_high, bollinger_low, bollinger_middle, close):
        self.log_returns = log_returns
        self.bollinger_high = bollinger_high
        self.bollinger_low = bollinger_low
        self.bollinger_middle = bollinger_middle
        self.close = close
       # assert isinstance(log_returns, LogReturns)

        super().__init__(feature_list=[log_returns, bollinger_high, bollinger_low, bollinger_middle, close])

    def compute(self, ii):

        lr = (self.close[ii] - self.bollinger_middle[ii])/(self.bollinger_high[ii] - self.bollinger_low[ii])
        sgn = (self.close[ii] - self.bollinger_middle[ii])/(self.bollinger_high[ii] - self.bollinger_low[ii]) * self.log_returns[ii]

        if lr > 0:
            self.allocation = 1

        else:
            self.allocation = -1

        return self.allocation
