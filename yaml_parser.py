import yaml
from string import Template
from db_connect import Connect
from rpc.rpc_bridge import RpcBridge
from rpc.db_bridge import DbBridge
from instance import Instance
import importlib


from data_retriever import *


def combine(terms, accum, res=[]):
    last = (len(terms) == 1)
    n = len(terms[0])
    for i in range(n):
        item = accum + terms[0][i] + "_"
        if last:
            res.append(item)
        else:
            combine(terms[1:], item, res)


def stringigy_properties(properties):
    pass


def trim_combined_properties(r):
    pass


def generate_alphas():

    with open("alpha.yaml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            f = open('alpha_template', 'r')
            dd = {'featureImport': '', 'featureList': '', 'featureInit': '', 'alphaName': ''}
            template = f.read()
            res = template.format(**dd)

            yy = {}
            for alpha_name, alpha_properties in data.items():
                features = alpha_properties['Features']
                all_features = []
                for feature_name, feature_properties in features.items():
                    #print(feature_properties)

                    f = [{key: v for key in feature_properties.keys()} for v in feature_properties[key]]
                    print(f)
                    break
                    # for i in range(len(features)):
                    #     for j in range(len(features[i])):
                    #         if i < len(features):
                    #             name += features[i+1][j]
                    #
                    # break

        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    generate_alphas()
    # a = [['ab', 'cd', 'ef'], ['12', '34', '56']]
    # ss = []
    # combine(a, '_', res=ss)

    # conn = Connect('data.db')
    #
    # cur = conn.cursor()
    #
    # symbol = 'BTCUSDT'
    # periods = ['1m', '5m', '15m', '30m', '1h', '4h']
    # exchange = 'binance'
    #
    # data1min = Get_all_cata_data(cur, symbol, 1)
    # data5min = Get_all_cata_data(cur, symbol, 5)
    # data15min = Get_all_cata_data(cur, symbol, 15)
    # data30min = Get_all_cata_data(cur, symbol, 30)
    # data1h = Get_all_cata_data(cur, symbol, 60)
    # data4h = Get_all_cata_data(cur, symbol, 240)
    #
    # js = {'symbols': [{'symbol': symbol, 'periods': periods, 'exchange': 'binance', 'state': 'watch',
    #                    'history': len(data1min), 'strategies': []}]}
    #
    # ii = Instance()
    #
    # db_bridge = DbBridge(ii)
    # db_bridge.instantiate(js)
    #
    # db_bridge.backfill(exchange, symbol, '1m', data1min)
    # db_bridge.backfill(exchange, symbol, '5m', data5min)
    # db_bridge.backfill(exchange, symbol, '15m', data15min)
    # db_bridge.backfill(exchange, symbol, '30m', data30min)
    # db_bridge.backfill(exchange, symbol, '1h', data1h)
    # db_bridge.backfill(exchange, symbol, '4h', data4h)
    #
    # raw_data_managers = ii.get_raw_data_managers()
    #
    # btc1min = raw_data_managers['binanceBTCUSDT1m']
    #
    # btc5min = raw_data_managers['binanceBTCUSDT5m']
    #
    # btc15min = raw_data_managers['binanceBTCUSDT15m']
    #
    # btc30min = raw_data_managers['binanceBTCUSDT30m']
    #
    # btc1h = raw_data_managers['binanceBTCUSDT1h']
    #
    # btc4h = raw_data_managers['binanceBTCUSDT4h']
    #
    # ff = {'name': 'StochRsiD', 'raw_data_manager': btc1min, 'p1': 10, 'p2': 5, 'p3': 5}
    #
    # class_ = getattr(importlib.import_module("feature." + ff['name'].lower()), ff['name'])
    #
    # del ff['name']
    #
    # ii = class_(**ff)
    #
    # ii.save_feature()

    #aal = [{'name':'blabla', 'raw_data_manager':i1, 'p1':i2, 'p2':i3} for i1 in [1,2,3] for i2 in [3,3,3] for i3 in [8,10, 101]]
    #print(aal)


