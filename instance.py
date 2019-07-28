from raw_data_manager import RawDataManager
from feature.sma import Sma


class Instance:

    def __init__(self, instance=None):
        self.instance = instance
        
        self.raw_data_managers = {}

        self.sma_test = None
    
    def set_instance(self, instance):
        self.instance = instance

    # can be accomplished by a factory class
    def create_raw_data_managers(self):
        symbols = self.instance.get('symbols')
        for symbol in symbols:
            periods = symbol.get('periods')
            for period in periods:
                exchange = symbol.get('exchange')
                ss = symbol.get('symbol')
                history = symbol.get('history')

                key = exchange + ss + period

                # don't forget to not actually hardcode the 256 lookback
                self.raw_data_managers[key] = RawDataManager(exchange, ss, period, 256, history)
    
    # backfill and update should probably be handled by a different object, good enough impl for now
    def backfill(self, exchange, symbol, period, data):
        key = exchange + symbol + period

        if self.raw_data_managers.get(key) != None:
            self.raw_data_managers[key].backfill(data)
        
        self.sma_test =Sma(100, 20, self.raw_data_managers['binanceBTCUSDT1m'])
        
        self.sma_test.backfill()
        
        #print('feature backfill... ')
        ff = self.sma_test.get_feature()
        #print(len(ff))
        print(ff[-1:])

    def update(self, exchange, symbol, period, data):
        key = exchange + symbol + period
        if self.raw_data_managers.get(key) != None:
            self.raw_data_managers[key].update(data)

        self.sma_test.update()
        
        print('feature update... ')
        ff = self.sma_test.get_feature()
        print(len(ff))
        print(ff[-2:])