from raw_data_manager import RawDataManager

class AbstractStrategy:

    def __init__(self, initial_allocation, pair, period, raw_data_managers, is_live=False, feature_list=None, model=None):
        self.pair = pair
        self.period = period
        self.model = model
        self.feature_list = feature_list
        self.is_live = is_live

        self.pnl = 0

        assert len(raw_data_managers) > 0

        # start computing strategy at index 0 of raw data is there are no feature that need lookback
        # if feature_list is None:
        #    self.index = 0
        # else:
            # start with strategy computation at the earliest, i.e after all features have enough data
        #    self.index = max([f.get_lookback() for f in feature_list]) - 1 

        self.raw_data_managers = raw_data_managers

        self.main_data_manager = None
        
        for m in raw_data_managers:
            assert isinstance(m, RawDataManager)
            # exchange should also be here
            if period == m.get_period() and pair == m.get_symbol():
                self.main_data_manager = m
                break
        
        assert self.main_data_manager is not None

        # self.time_data = self.main_data_manager.get_backfill_data().get('time')
        
        # prediction format 
        self.allocation = initial_allocation

    # override dis ... 
    def compute(self, ii):
        return self.allocation

    def get_main_data_manager(self):
        return self.main_data_manager

    def get_earliest_start_time(self):
        if len(self.feature_list) == 0:
            return self.main_data_manager.get_backfill_data()['time'][0]
        
        dates = []
        for f in self.feature_list:
            dd = f.get_DF()
            # print(dd.index)
            dates.append(dd.index[0])
        
        return max(dates)
