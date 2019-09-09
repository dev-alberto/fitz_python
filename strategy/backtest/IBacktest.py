from abc import ABCMeta, abstractmethod

class IBacktestAble(metaclass=ABCMeta):
    
    @abstractmethod
    def backfill(self,time_index):
        pass

    @abstractmethod
    def get_earliest_start_time(self):
        pass

    @abstractmethod
    def get_main_data_manager(self):
        pass


