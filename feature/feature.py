from numpy_ringbuffer import RingBuffer
from collections.abc import Sequence

from collections import OrderedDict

import numpy as np
import pandas as pd
import csv
import os
import inspect


class EmptyFeature(Sequence):
    def __init__(self, lookback, raw_data_manager, name="", backfill=True, history_lengh=None, features=None):
        raw_data_length = raw_data_manager.get_history()

        # kind of spaghetti logic here to for feature history length but the gist is this:
        # one may specify history length when instantiating or we can produce the maximum 
        # length given the data available
        feath = 0
        hh = raw_data_length

        if features is not None:
            feath = min([f.get_history_length() for f in features])
            hh = feath

        if history_lengh is None:
            self.history_lengh = hh - lookback + 1
        else:
            self.history_lengh = history_lengh

        self.lookback = lookback

        self.raw_data_manager = raw_data_manager

        # raw data must be able to fill history
        assert (self.history_lengh + lookback - 1) <= raw_data_length
        assert lookback <= raw_data_manager.get_lookback()

        self.feature = OrderedDict()

        self.feature_numpy = RingBuffer(capacity=self.history_lengh, dtype=np.float64)

        self.latest = {}

        # a feature may contain multiple features
        self.features = features

        self.feature_df = raw_data_manager.get_backfill_df()

        # trim df
        drop_i = self.lookback
        if self.features is not None:
            if len(self.features) > 0:
                drop_i = drop_i + max([f.get_lookback() for f in self.features]) - 1

        self.feature_df = self.feature_df.iloc[(drop_i - 1):]

        # must take into account history len;

        if backfill:
            self.backfill()

        self.live_save_path = 'data_test/live/features/' + type(self).__name__ + '.csv'

        self.backtest_path = 'data_test/features/' + self.__str__() + name + '.csv'

        # self.save_feature()

        self.test_rounded = []

        super().__init__()

    def get_feature(self):
        # assert len(self.feature) > 0
        return self.feature

    def get_history_length(self):
        return self.history_lengh

    # -> override this ... 
    def compute(self, data_dict):
        return []

    def populate_feature(self):
        l = len(self.get_TS())
        c = 0
        for index, value in self.get_TS().items():
            self.feature_numpy.append(value)
            self.feature[index] = value
            if c == l - 1:
                self.latest = {'time': index, 'value': value}
            c += 1

    def update_feature(self, time, value):

        # we remove first item in dict, add the new one, FIFO style
        # maybe use hist length?
        if len(self.feature) > self.history_lengh:
            self.feature.popitem(last=False)

        self.feature[time] = value

        self.feature_numpy.append(value)

        # assert len(self.feature) == self.history_lengh

    # backfill history
    def backfill(self):

        data = self.raw_data_manager.get_backfill_data()
        ff = self.compute(data)[-self.history_lengh:]

        print(len(ff))
        print(self.history_lengh)

        assert len(ff) == self.history_lengh

        self.feature_df[str(self)] = ff

        self.populate_feature()

    # live update
    def update(self):
        candle = self.raw_data_manager.get_live_candle()
        time_stamp = candle.get('time')

        # update sub-features
        if self.features is not None:
            for f in self.features:
                f.update()

        # check as to not duplicate update
        if time_stamp in self.feature:
            return

        # print('Updating ... ' + type(self).__name__)

        data = self.raw_data_manager.get_live_data()

        new_val = self.compute(data)[-1]

        self.latest = {'time': time_stamp, 'value': new_val}

        self.update_feature(time_stamp, new_val)

        # self.save_feature_live()

    def __getitem__(self, i):

        rounded_ii = self.get_rounded_index(i)
        if rounded_ii in self.feature:
            return self.feature[rounded_ii]
        else:
            print("Feature is... ")
            print(type(self).__name__)
            print("Actual index ")
            print(i)
            print("Rounded ")
            print(rounded_ii)
            print("First keys")
            kk = list(self.feature.keys())
            print(kk[0:10])

        raise ValueError("Feature timestamp not found")

    def get_last_timestamp(self):
        return next(reversed(self.feature))

    def get_rounded_index(self, index):
        per_minutes = self.raw_data_manager.get_period_in_minutes()
        return index - (index//60 % per_minutes) * 60

    def get_period(self):
        return self.raw_data_manager.get_period()

    def __len__(self):
        return len(self.feature)

    def __eq__(self, other_feature):
        return isinstance(other_feature, EmptyFeature) and type(self).__name__ == type(other_feature).__name__ \
               and self.raw_data_manager == other_feature.raw_data_manager

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return type(self).__name__ + self.raw_data_manager.get_symbol() + self.get_period()

    def get_history_start_time(self):
        # return self.feature_df.index[0]
        return next(iter(self.feature))

    def get_DF(self):
        return self.feature_df

    def get_TS(self):
        return self.feature_df[str(self)]

    def get_numpy(self):
        return self.feature_numpy

    # Use this method especially ifm for example
    #  in an alpha that updates every 1 minute you need a feature that updates every 5m.
    # If not used, feature[ii] will give a value error in that instance
    def get_latest(self):
        return self.latest

    def get_lookback(self):
        return self.lookback

    def save_DF(self):
        name = type(self).__name__ + '.csv'
        self.feature_df.to_csv('data_test/features/' + name)

    def save_feature(self):
        if os.path.isfile(self.backtest_path):
            return

        feature_file = open(self.backtest_path, 'w+')

        writer = csv.DictWriter(feature_file, fieldnames=['time', 'value'])
        writer.writeheader()

        for ts, val in self.feature.items():
            writer.writerow({'time': ts, 'value': val})

    def save_feature_live(self):
        strategy_file = open(self.live_save_path, 'a')

        writer = csv.DictWriter(strategy_file, fieldnames=['time', 'value'])

        writer.writerow(self.latest)
