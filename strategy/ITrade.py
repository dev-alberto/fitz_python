from abc import ABCMeta, abstractmethod

class ITradeAble(metaclass=ABCMeta):
    
    @abstractmethod
    def generate_position(self, ii):
        pass

