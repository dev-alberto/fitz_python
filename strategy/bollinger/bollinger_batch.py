from strategy.batch import Batch

from strategy.bollinger.boll2 import BollingerImpl2

from feature.crosscbl import CrossCbl
from feature.crossbhc import CrossBHc

from feature.bollingerlow import BollingerLow
from feature.bollingerhigh import BollingerHigh
from feature.bollingermiddle import BollingerMiddle
from feature.logreturns import LogReturns
from feature.close import Close


class BollingerBatch(Batch):

    def __init__(self, raw_data_manager, ticker=None):
        
        per = [20, 15, 25, 30]
        std = [2.5, 3]

        alphas = []

        for p in per:
            for s in std:

                close = Close(raw_data_manager)

                bl = BollingerLow(p, s, raw_data_manager)

                bh = BollingerHigh(p, s, raw_data_manager)

                bm = BollingerMiddle(p, s, raw_data_manager)

                log_r = LogReturns(5, raw_data_manager)

                cross_cbl = CrossCbl(bl, raw_data_manager)

                cross_bhc = CrossBHc(bh, raw_data_manager)

                bollinger_alpha = BollingerImpl2(log_r, bh, bl, bm, close, raw_data_manager)

                alphas.append(bollinger_alpha)

        print(len(alphas))

        super().__init__(alphas, ticker=ticker)
