from raw_data_manager import RawDataManager
from strategy.ITrade import TradeAble
from feature.feature import EmptyFeature
from collections import OrderedDict
import csv


class Alpha(TradeAble):
    def __init__(self, feature_list=None, model=None, init_alloc=0, history=1000000):

        assert feature_list is not None
        assert len(feature_list) > 0
        # self.pair = pair
        # self.period = period
        self.model = model
        self.feature_list = feature_list

        self.history = history

        # assert len(raw_data_managers) > 0

        #self.raw_data_managers = raw_data_managers

        # daprint('Abstract class raw data managers: ')
        # print(raw_data_managers)

        # self.main_data_manager = None
        #
        # for m in raw_data_managers:
        #     assert isinstance(m, RawDataManager)
        #     # exchange should also be here
        #     if period == m.get_period() and pair == m.get_symbol():
        #         self.main_data_manager = m
        #         break
        #
        # assert self.main_data_manager is not None

        # print("main data manager in abstract class is... ")
        # print(self.main_data_manager)

        self.allocation = init_alloc

        self.start_time = self.get_earliest_start_time()

        self.alpha = OrderedDict()
        self.alpha[self.start_time] = init_alloc

        self.cumulative_pnl = 0

        self.change_position_pnl = 0

        # self.backfillData = self.main_data_manager.get_backfill_df()

        # comment once logs no longer needed
        # self.csv_path = 'data_test/live/alphas/' + type(self).__name__ + '.csv'
        #
        # alpha_file = open(self.csv_path, 'w+')
        # row, fieldnames = self.create_log_row(0, 0)
        # writer = csv.DictWriter(alpha_file, fieldnames=fieldnames)
        # writer.writeheader()
        # writer.writerow(row)
        # alpha_file.close()

        super().__init__(self.alpha)

    # def create_log_row(self, current_pnl, cum_pnl):
    #     r = self.main_data_manager.get_latest()
    #
    #     r['allocation'] = self.allocation
    #
    #     for f in self.feature_list:
    #         name = str(f)
    #         first_vals = f.get_latest()
    #         r[name] = first_vals['value']
    #         # r[name + '_time'] = first_vals['time']
    #
    #     r['returns'] = current_pnl
    #     r['pnl'] = cum_pnl
    #
    #     fieldnames = list(r.keys())
    #
    #     return r, fieldnames

    def backfill(self, time_index):
        print(len(time_index))
        for ii in time_index:
            self.alpha[ii] = self.generate_position(ii)
           # self.alpha[ii] = self.compute(ii)
        return self.alpha

    def generate_position(self, ii):

        #self.update_features()

        # compute pnl before overriding self.allocation,
        # but just after finding last candle close
        #pnl = self.allocation * (self.main_data_manager.get_latest()['close'] - self.main_data_manager.get_latest()['open'])
        #pnl = self.allocation * (
        #            self.backfillData['close'][ii] - self.backfillData['open'][ii])

        # print('pnl1')
        # print(pnl)

        #self.cumulative_pnl += pnl
        #self.change_position_pnl += pnl

        prev = self.allocation

        position = self.compute(ii)
        if prev != position:
            # print(self.change_position_pnl)
            self.change_position_pnl = 0

        if len(self.alpha) > self.history:
            self.alpha.popitem(last=False)

        self.alpha[ii] = position

        # alpha_file = open(self.csv_path, 'a')
        # row, fieldnames = self.create_log_row(pnl, self.cumulative_pnl)
        #
        # writer = csv.DictWriter(alpha_file, fieldnames=fieldnames)
        # writer.writerow(row)
        # alpha_file.close()

        return position

    def compute(self, ii):
        return self.allocation

    def update_features(self):
        if self.feature_list is not None:
            for f in self.feature_list:
                f.update()

    def get_earliest_start_time(self):

        dates = []
        for f in self.feature_list:
            dd = f.get_history_start_time()
            #print("*****")
            #print(dd)
            dates.append(dd)

        return max(dates)

    def get_last_time_index(self):

        dates = []
        for f in self.feature_list:
            dd = f.get_last_timestamp()
            #print(dd.index)
            dates.append(dd)
        return min(dates)

    # def get_main_data_manager(self):
    #     return self.main_data_manager

    def get_features(self):
        return self.feature_list

    def get_history_len(self):
        return self.history

    def run_data_tests(self):
        pass

