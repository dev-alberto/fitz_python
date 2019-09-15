from strategy.batch import Batch

from strategy.bollinger.boll1 import BollingerImpl1

from feature.cross_cbl import Cross_cBL
from feature.cross_bhc import Cross_BHc

from feature.bollinger_low import BollingerLow
from feature.bollinger_high import BollingerHigh


class BollingerBatch(Batch):

    def __init__(self, raw_data_manager, ticker=None):
        
        per = [40, 60, 90, 120]
        std = [2, 3]

        alphas = []

        for p in per:
            for s in std:

                bl = BollingerLow(p, s, raw_data_manager)

                bh = BollingerHigh(p, s, raw_data_manager)

                cross_cbl = Cross_cBL(bl, raw_data_manager)

                cross_bhc = Cross_BHc(bh, raw_data_manager)

                bollinger_alpha = BollingerImpl1(cross_cbl, cross_bhc, raw_data_manager)

                alphas.append(bollinger_alpha)

        print(len(alphas))

        super().__init__(alphas, ticker=ticker)
