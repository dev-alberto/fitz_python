from rpc.bridge_interface import IBridge
from instance import Instance

class RpcBridge(IBridge):

    def __init__(self, instance_obj):
        
        assert isinstance(instance_obj, Instance)
        self.instance_obj = instance_obj

    def instantiate(self, instance):
        
        self.instance_obj.set_instance(instance)

        self.instance_obj.create_tickers_and_raw_data_managers()

        return 'Ok, I have instantiated'

    def create_ticker(self, symbol, exchange):
        
        print(symbol)

        self.instance_obj.create_ticker(symbol, exchange)
        
        return 'Ok, I have created ticker'

    def backfill(self, exchange, symbol, period,  data):

        self.instance_obj.backfill(exchange, symbol, period,  data)

        return 'Ok, I have backfilled'

    def live_update(self, exchange, symbol, period,  data):
        
        assert len(data) == 1

        pos1 = self.instance_obj.update(exchange, symbol, period,  data)

        # will probably return alloc
        return pos1

    def update_ticker(self, symbol, exchange, ticker):
        #print(ticker)

        self.instance_obj.update_ticker(symbol, exchange, ticker)
        
        return 'Ok, I have updated ticker'
