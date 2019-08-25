import numpy as np

from db_connect import Connect
from rpc.rpc_bridge import RpcBridge
from rpc.db_bridge import DbBridge
from instance import Instance

from feature.vwap import Vwap
from feature.returns import Returns
from feature.mean_returns import MeanReturns

from data_retriever import Get_all_candles, Get_candlesticks_between_dates


if __name__ == '__main__':
    
    conn = Connect('fitz.db')
    cur = conn.cursor()

    symbol = 'BTCUSDT'
    period = '1m'
    exchange = 'binance'

    data = Get_candlesticks_between_dates(cur, "2019-7-12-17-0-0", "2019-7-16-18-0-0", period,symbol,exchange)
    
    js = {'symbols': [{'symbol': symbol, 'periods': ['1m'], 'exchange': 'binance', 'state': 'watch', 'history': len(data),'strategies': []}]}

    ii = Instance()
    
    db_bridge = DbBridge(ii)
    db_bridge.instantiate(js)

    db_bridge.backfill(exchange, symbol, period, data)

    raw_data_managers = ii.get_raw_data_managers()

    btc1min = raw_data_managers['binanceBTCUSDT1m']

    btc1min.sava_backfill_to_disk('data_test/file1.csv')

    r = Returns(20, btc1min)

    r.backfill()

    r.save_DF()

    #mean_r = MeanReturns(5, btc1min, r)

    #mean_r.backfill()

    #ff = mean_r.get_feature()

    #print(min(ff))

    #print(max(ff))