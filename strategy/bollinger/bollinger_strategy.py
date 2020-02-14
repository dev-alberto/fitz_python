from strategy.bollinger.boll1 import BollingerImpl1
from strategy.bollinger.boll2 import BollingerImpl2
from strategy.bollinger.boll3 import BollingerImpl3
from strategy.bollinger.boll4 import BollingerImpl4
from raw_data_manager import RawDataManager

from feature.crosscbl import CrossCbl
from feature.crossbhc import CrossBHc
from  feature.logreturns import LogReturns
from feature.crosscbh import CrossCbh
from feature.crossbmc import CrossBmc
from feature.crosscbm import CrossCbm
from  feature.close import Close
from feature.crossblc import CrossBLc

from feature.bollingerlow import BollingerLow
from feature.bollingerhigh import BollingerHigh
from feature.bollingermiddle import BollingerMiddle

from strategy.strategy import AbstractStrategy


class BollingerStrategy(AbstractStrategy):

    def __init__(self, raw_data_manager, ticker=None):

        assert isinstance(raw_data_manager, RawDataManager)

        #assert raw_data_manager.get_period() == '1m' and raw_data_manager.get_symbol() == 'BTCUSDT'

        bl = BollingerLow(20, 3, raw_data_manager)

        bh = BollingerHigh(20, 3, raw_data_manager)

        bm = BollingerMiddle(90, 3, raw_data_manager)

        cross_cbl = CrossCbl(bl, raw_data_manager)

        cross_bhc = CrossBHc(bh, raw_data_manager)

        cross_cbh = CrossCbh(bh, raw_data_manager)

        close = Close(raw_data_manager)

        # cross_bmc = CrossBmc(bm, raw_data_manager)

        # cross_cbm = CrossCbm(bm, raw_data_manager)

        log_r = LogReturns(5, raw_data_manager)

        cross_blc = CrossBLc(bl, raw_data_manager)

        bollinger1 = BollingerImpl1(cross_cbl, cross_bhc)

        bollinger2 = BollingerImpl2(log_r, bh, bl, bm, close)

        bollinger3 = BollingerImpl3(cross_cbl, cross_bhc, cross_cbh, cross_blc)

        # bollinger4 = BollingerImpl4(cross_cbl, cross_bhc, cross_cbh, cross_blc, cross_bmc, cross_cbm)

        #weights = {bollinger1: 0.33, bollinger2: 0.34, bollinger3: 0.33}

        weights  = {bollinger1: 1}

        super().__init__(raw_data_manager, weights, ticker=ticker)

