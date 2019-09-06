from strategy.live_strategy import AbstractLiveStrategy
from strategy.bollinger.boll1 import BollingerImpl1

from raw_data_manager import RawDataManager

from feature.cross_cbl import Cross_cBL
from feature.cross_bhc import Cross_BHc

from feature.bollinger_low import BollingerLow
from feature.bollinger_high import BollingerHigh


class BollingerLive(AbstractLiveStrategy):

    def __init__(self, size, raw_data_manager, ticker):
        
        #btc1min = raw_data_managers['binanceBTCUSDT1m']

        assert isinstance(raw_data_manager, RawDataManager)

        assert raw_data_manager.get_period() == '1m' and raw_data_manager.get_symbol() == 'BTCUSDT'


        bl = BollingerLow(90, 3, raw_data_manager)

        bh = BollingerHigh(90, 3, raw_data_manager)

        cross_cbl = Cross_cBL(bl, raw_data_manager)

        cross_bhc = Cross_BHc(bh, raw_data_manager)

        bollinger1 = BollingerImpl1(cross_cbl, cross_bhc, raw_data_manager,is_live=True)

        super().__init__(size=size, raw_data_manager=raw_data_manager, ticker=ticker,strategies=[bollinger1], features=[bl,bh,cross_cbl,cross_bhc])

        self.strategy_weights[bollinger1] = 1
