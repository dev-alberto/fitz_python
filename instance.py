from raw_data_manager import RawDataManager
from ticker import Ticker

import time

from strategy.bollinger_live import BollingerLive

class Instance:

    def __init__(self, instance=None):
        self.instance = instance
        
        self.raw_data_managers = {}

        self.tickers = {}

        self.live_bollinger = None
    
    def set_instance(self, instance):
        self.instance = instance


    # can be accomplished by a factory class
    def create_tickers_and_raw_data_managers(self):
        symbols = self.instance.get('symbols')
        for symbol in symbols:
            periods = symbol.get('periods')
            for period in periods:
                exchange = symbol.get('exchange')
                ss = symbol.get('symbol')
                history = symbol.get('history')

                raw_manager_key = exchange + ss + period
                ticker_key = exchange + ss
                
                if ticker_key not in self.tickers:
                    self.tickers[ticker_key] = Ticker(256, exchange, symbol, 0, 0, int(round(time.time() * 1000)))
                
                if raw_manager_key not in self.raw_data_managers:
                    # don't forget to not actually hardcode the 256 lookback
                    self.raw_data_managers[raw_manager_key] = RawDataManager(exchange, ss, period, 256, history)

    # backfill and update should probably be handled by a different object, good enough impl for now
    def backfill(self, exchange, symbol, period, data):
        key = exchange + symbol + period

        if self.raw_data_managers.get(key) != None:
            self.raw_data_managers[key].backfill(data)
        
        # instatiate strategy here? Yeah.. Check which raw data managers have been backfilled first ... 

        if key == 'binanceBTCUSDT1m':
            ticker_key = exchange + symbol
            assert ticker_key in self.tickers

            self.live_bollinger = BollingerLive(1000, self.raw_data_managers[key], self.tickers[ticker_key])


    def update(self, exchange, symbol, period, data):
        key = exchange + symbol + period
        #print('Updating ... ' + key)
        #print(data)
        if self.raw_data_managers.get(key) != None:
            self.raw_data_managers[key].update(data)

        # for different strategies, will need to update proper strategies, depending on key
        ii = self.raw_data_managers[key].get_live_candle().get('time')
        return self.live_bollinger.generate_position(ii)

    def update_ticker(self, symbol, exchange, ticker):
        key = exchange + symbol

        self.tickers[key].update(ticker)

    def get_raw_data_managers(self):
        return self.raw_data_managers
