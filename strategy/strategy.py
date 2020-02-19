from data.raw_data_manager import RawDataManager
from data.ticker import Ticker
from strategy.ITrade import TradeAble
from collections import OrderedDict
import csv


# add book info, as well as other factors
class AbstractStrategy(TradeAble):

    def __init__(self, raw_data_manager, alphas, ticker=None, init_alloc=0):

        assert isinstance(raw_data_manager, RawDataManager)
        
        if ticker is not None:    
            assert isinstance(ticker, Ticker)

        assert isinstance(alphas, dict)
        
        self.raw_data_manager = raw_data_manager

        self.alphas = alphas

        self.ticker = ticker

        self.init_alloc = init_alloc

        self.start_time = self.get_earliest_start_time()

        self.history = min([a.get_history_len() for a in self.alphas.keys()])

        self.position = init_alloc

        self.strategy = OrderedDict()
        self.strategy[self.start_time] = init_alloc

        self.cumulative_pnl = 0

        # LOGS; remove for actual live ...
        # self.csv_path = 'data_test/live/strategies/' + type(self).__name__ + '.csv'
        # self.fieldnames = self.create_strategy_log_get_fieldnames()

        super().__init__(self.strategy)

    # for backtest purpose only
    def backfill(self, time_index):

        # backfill alphas
        for k in self.alphas.keys():
            k.backfill(time_index)

        for index in time_index:
            position = 0
            
            for a, w in self.alphas.items():
                #print('here')
                alloc = a[index]
                position += alloc * w

            self.strategy[index] = position

        return self.strategy

    def create_strategy_log_get_fieldnames(self):
        alpha_names = [type(list(self.alphas.keys())[i]).__name__ for i in range(len(self.alphas))]

        strategy_file = open(self.csv_path, 'w+')

        r1 = self.raw_data_manager.get_latest()

        for k in alpha_names:
            r1[k] = self.init_alloc

        r1['strategy'] = 0
        r1['bid'] = 0
        r1['ask'] = 0
        r1['pnl'] = 0
        r1['position'] = self.init_alloc

        fieldnames = list(r1.keys())

        writer = csv.DictWriter(strategy_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow(r1)

        return fieldnames

    def generate_position(self, ii):

        self.cumulative_pnl += self.position * (self.raw_data_manager.get_latest()['close'] - self.raw_data_manager.get_latest()['open'])

        # log = {'pnl': self.cumulative_pnl}

        position = 0

        for a, w in self.alphas.items():
            alloc = a.generate_position(ii)
            position += alloc * w

            # log[type(a).__name__] = alloc

        if len(self.strategy) > self.history:
            self.strategy.popitem(last=False)
        
        self.strategy[ii] = position
        self.position = position

        # log['position'] = position
        #
        # llog = {**log, **self.raw_data_manager.get_latest()}
        #
        # strategy_file = open(self.csv_path, 'a')
        #
        # writer = csv.DictWriter(strategy_file, fieldnames=self.fieldnames)
        #
        # # compare bid ask with next open maybe ?
        # llog['bid'] = self.ticker.get_bid()
        # llog['ask'] = self.ticker.get_ask()
        #
        # writer.writerow(llog)

        return position

    def get_earliest_start_time(self):
        dates = []
        for alpha in self.alphas.keys():
            dd = alpha.get_earliest_start_time()
            dates.append(dd)
        
        return max(dates)

    def get_last_time_index(self):
        dates = []
        for alpha in self.alphas.keys():
            dd = alpha.get_last_time_index()
            dates.append(dd)

        return min(dates)

    #def get_main_data_manager(self):
    #    print("function is called with data manager ")
    #    print(self.raw_data_manager)
    #    return self.raw_data_manager

    def run_data_tests(self):
        for alpha in self.alphas.keys():
            alpha.run_data_tests()
