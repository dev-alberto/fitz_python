from rpc.bridge_interface import IBridge

class RpcBridge(IBridge):

    def __init__(self, instance_obj):
        self.instance_obj = instance_obj

    def instantiate(self, instance):
        print(instance)
        self.instance_obj.set_instance(instance)

        self.instance_obj.create_raw_data_managers()

        return 'Ok, I have instantiated'

    def backfill(self, exchange, symbol, period,  data):

        self.instance_obj.backfill(exchange, symbol, period,  data)

        return 'Ok, I have backfilled'

    def live_update(self, exchange, symbol, period,  data):
        assert len(data) == 1

        self.instance_obj.update(exchange, symbol, period,  data)

        # will return predion of course
        return 'Ok, I have updated'
