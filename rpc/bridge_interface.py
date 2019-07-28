from abc import ABCMeta, abstractmethod

class IBridge(metaclass=ABCMeta):
    
    @abstractmethod
    def instantiate(self, instance):
        pass

    @abstractmethod
    def backfill(self, exchange, symbol, period,  data):
        pass

    @abstractmethod
    def live_update(self, exchange, symbol, period,  data):
        pass
