import numpy as np
import pandas as pd

from db_connect import Connect
from rpc.rpc_bridge import RpcBridge
from rpc.db_bridge import DbBridge
from instance import Instance

from raw_data_manager import RawDataManager

from feature.close import Close

from feature.bollinger_high import *
from feature.bollinger_low import *
from feature.cross_bhc import *
from feature.cross_cbl import *


from feature.LogReturns import LogReturns

from data_retriever import *


if __name__ == '__main__':
    
    conn = Connect('fitz.db')
    cur = conn.cursor()

    symbol = 'BTCUSDT'
    period = '1m'
    exchange = 'binance'

    #data = Get_candlesticks_between_dates(cur, "2019-7-12-17-0-0", "2019-7-16-18-0-0", period,symbol,exchange)
    data = Get_all_candlesticks_with_period(cur, period, symbol, exchange)
    js = {'symbols': [{'symbol': symbol, 'periods': ['1m'], 'exchange': 'binance', 'state': 'watch', 'history': len(data),'strategies': []}]}

    ii = Instance()
    
    db_bridge = DbBridge(ii)
    db_bridge.instantiate(js)

    db_bridge.backfill(exchange, symbol, period, data)

    raw_data_managers = ii.get_raw_data_managers()

    btc1min = raw_data_managers['binanceBTCUSDT1m']

    assert isinstance(btc1min, RawDataManager)
    
    time = btc1min.get_backfill_data()['time']

    #print('Time: ')
    #print(time[0:5])
    #print('********')
    #print(time[-5:])

    #r = LogReturns(5, btc1min)

    #r_ts = list(r.get_feature().keys())

    #print('Log Ret: ')
    #print(r_ts[0:5])
    #print('********')
    #print(r_ts[-5:])

    #bl = BollingerLow(90, 3, btc1min)

    #bh = BollingerHigh(90, 3, btc1min)

    #cross_cbl = Cross_cBL(bl, btc1min)

    #cross_bhc = Cross_BHc(bh, btc1min)

    #dd1 = bl.get_DF()

    #dd2 = cross_cbl.get_DF()

    cl = Close(btc1min)

    print(cl.get_DF().head(5))