from strategy.strategy import AbstractStrategy
from strategy.bollinger.boll1 import BollingerImpl1
from strategy.bollinger.boll2 import BollingerImpl2
from strategy.bollinger.boll3 import BollingerImpl3
from strategy.bollinger.boll4 import BollingerImpl4

from raw_data_manager import RawDataManager

from feature.cross_cbl import Cross_cBL
from feature.cross_bhc import Cross_BHc
from feature.cross_cbh import Cross_cBH
from feature.cross_bmc import Cross_BMc
from feature.cross_cbm import Cross_cBM
from feature.cross_blc import Cross_BLc

from feature.bollinger_low import BollingerLow
from feature.bollinger_high import BollingerHigh
from feature.bollinger_middle import BollingerMiddle


class BollingerStrategy(AbstractStrategy):

    def __init__(self, raw_data_manager, ticker=None):

        assert isinstance(raw_data_manager, RawDataManager)

        #assert raw_data_manager.get_period() == '1m' and raw_data_manager.get_symbol() == 'BTCUSDT'

        bl = BollingerLow(20, 3, raw_data_manager)

        bh = BollingerHigh(20, 3, raw_data_manager)

        # bm = BollingerMiddle(90, 3, raw_data_manager)

        cross_cbl = Cross_cBL(bl, raw_data_manager)

        cross_bhc = Cross_BHc(bh, raw_data_manager)

        cross_cbh = Cross_cBH(bh, raw_data_manager)

        # cross_bmc = Cross_BMc(bm, raw_data_manager)

        # cross_cbm = Cross_cBM(bm, raw_data_manager)

        cross_blc = Cross_BLc(bl, raw_data_manager)

        bollinger1 = BollingerImpl1(cross_cbl, cross_bhc, raw_data_manager)

        bollinger2 = BollingerImpl2(cross_cbl, cross_bhc, cross_cbh,raw_data_manager)

        bollinger3 = BollingerImpl3(cross_cbl, cross_bhc, cross_cbh, cross_blc, raw_data_manager)

        # bollinger4 = BollingerImpl4(cross_cbl, cross_bhc, cross_cbh, cross_blc, cross_bmc, cross_cbm, raw_data_manager)

        weights = {bollinger1: 0.33, bollinger2: 0.34, bollinger3: 0.33}

        # weights  = {bollinger2:1}

        super().__init__(raw_data_manager, weights, ticker=ticker)
