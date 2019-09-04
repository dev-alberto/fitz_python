from db_connect import Connect
from rpc.rpc_bridge import RpcBridge
from rpc.db_bridge import DbBridge
from instance import Instance

from data_retriever import *

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


if __name__ == '__main__':
    
    conn = Connect('fitz.db')
    cur = conn.cursor()

    symbol = 'BTCUSDT'
    period = '1m'
    exchange = 'binance'

    data1 = Get_candlesticks_between_dates(cur, "2019-7-12-17-0-0", "2019-7-16-18-0-0", period,symbol,exchange)
    
    data2 = Get_all_candlesticks_with_period(cur, period, symbol, exchange)

    start = Get_datetime_from_miliseconds(data2[0]['time'])
    end =  Get_datetime_from_miliseconds(data2[-1]['time'])

    print(start, end)

