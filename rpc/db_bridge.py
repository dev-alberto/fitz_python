from rpc.bridge_interface import IBridge
from instance import Instance


# there should probably be an interface for this, to achieve dependecy inversion.
# Testing features without needing to connect to the node JS portion should be possible
class DbBridge(IBridge):

    def __init__(self, instance_obj):
        assert isinstance(instance_obj, Instance)
        self.instance_obj = instance_obj

    def instantiate(self, instance):
        self.instance_obj.set_instance(instance)

        self.instance_obj.create_tickers_and_raw_data_managers()

        print('Ok, I have instantiated')

    def backfill(self, exchange, symbol, period,  data):

        self.instance_obj.backfill(exchange, symbol, period,  data)

        print('Ok, I have backfilled')

    def live_update(self, exchange, symbol, period,  data):
        assert len(data) == 1

        self.instance_obj.update(exchange, symbol, period,  data)

        # will return predion of course
        print('Ok, I have updated')
