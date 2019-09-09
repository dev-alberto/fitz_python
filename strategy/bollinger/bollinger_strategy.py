from strategy.strategy import AbstractStrategy
from strategy.bollinger.boll1 import BollingerImpl1

from raw_data_manager import RawDataManager

from feature.cross_cbl import Cross_cBL
from feature.cross_bhc import Cross_BHc

from feature.bollinger_low import BollingerLow
from feature.bollinger_high import BollingerHigh


class BollingerStrategy(AbstractStrategy):

    def __init__(self, raw_data_manager, ticker=None):

        assert isinstance(raw_data_manager, RawDataManager)

        assert raw_data_manager.get_period() == '1m' and raw_data_manager.get_symbol() == 'BTCUSDT'


        bl = BollingerLow(90, 3, raw_data_manager)

        bh = BollingerHigh(90, 3, raw_data_manager)

        cross_cbl = Cross_cBL(bl, raw_data_manager)

        cross_bhc = Cross_BHc(bh, raw_data_manager)

        bollinger1 = BollingerImpl1(cross_cbl, cross_bhc, raw_data_manager)

        super().__init__(raw_data_manager, {bollinger1:1}, ticker=ticker)
