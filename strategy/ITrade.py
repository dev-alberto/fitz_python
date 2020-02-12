from collections.abc import Sequence
from strategy.backtest.IBacktest import IBacktestAble


class TradeAble(Sequence, IBacktestAble):

    def __init__(self, position_dict):
        self.positions = position_dict
        pass

    def __getitem__(self, index):
        return self.positions[index]

    def __len__(self):
        return len(self.positions)

    def __eq__(self, other):
        return isinstance(other, TradeAble) and type(self).__name__ == type(other).__name__

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return str(self.positions)

    #def get_main_data_manager(self):
    #    pass

    def get_earliest_start_time(self):
        pass

    def get_last_time_index(self):
        pass

    def backfill(self, time_index):
        pass

    def run_data_tests(self):
        pass
