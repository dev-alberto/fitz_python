from instance import Instance
from rpc.db_bridge import DbBridge
import json
import os
from data.data_retriever import *
from data.db_connect import Connect
import pickle


def transform_period_to_minutes(pp):
    assert isinstance(pp, str)
    if pp.endswith("m"):
        return int(pp[:-1])

    if pp == '1h':
        return 60
    if pp == '2h':
        return 120
    elif pp == '4h':
        return 240
    elif pp == '6h':
        return 360
    elif pp == '12h':
        return 720
    elif pp == '1d':
        return 1440
    elif pp == '1w':
        return 10080


def backfill_agg_cata_data():
    conn = Connect('../data.db')
    cur = conn.cursor()

    for p in periods:
        minutes = transform_period_to_minutes(p)
        data_ = Get_all_cata_data(cur, symbol, minutes)
        db_bridge.backfill(exchange, symbol, p, data_)


def backfill_gecko_data():
    conn = Connect('../binance_0.1.db')
    cur = conn.cursor()

    for p in periods:
        minutes = transform_period_to_minutes(p)
        data_ = Get_all_gecko_data(cur, symbol, minutes)
        db_bridge.backfill(exchange, symbol, p, data_)


# returns raw_data_managers_dict with keys only the period, as {'1m':raw_data_manager}; path should be store/managers.p
def Get_period_only_managers(path_):
    path = 'config.json'
    if not os.path.isfile(path):
        raise ValueError('Config not found')
    f = open(path, "r")
    data = json.loads(f.read())
    symbol = data['symbols'][0]['symbol']
    exchange = data['symbols'][0]['exchange']

    dd = pickle.load(open(path_, "rb"))

    return {k.strip(exchange+symbol): v for (k, v) in dd.items()}


if __name__ == '__main__':
    pass

    # path = '../config.json'
    #
    # if not os.path.isfile(path):
    #     raise ValueError('Config not found')
    #
    # f = open(path, "r")
    # data = json.loads(f.read())
    # ii = Instance()
    # db_bridge = DbBridge(ii)
    # db_bridge.instantiate(data)
    #
    # periods = data['symbols'][0]['periods']
    # symbol = data['symbols'][0]['symbol']
    # exchange = data['symbols'][0]['exchange']

    # backfill_agg_cata_data()
    # backfill_gecko_data()
    # save_path = "store/" + exchange + symbol + ".p"
    # print(save_path)
    # pickle.dump(raw_data_managers, open(save_path, "wb"))


