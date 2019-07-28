from db_connect import Connect
from rpc.rpc_bridge import RpcBridge
from rpc.db_bridge import DbBridge
from instance import Instance

from data_retriever import Get_all_candles, Get_candlesticks_between_dates
import pandas as pd
import numpy as np
import tulipy as ti
import zerorpc

#    conn = Connect('fitz.db')

#    cur = conn.cursor()
#    rows = Get_candlesticks_between_dates(cur, "2019-7-16-17-0-0", "2019-7-16-18-0-0", '1m','BTCUSDT','binance')
#    df = candlesticks_to_pd(rows)

    # DATA = np.array([3, 5, 10, 15, 20, 25], dtype=np.float64) 

#    close = df['close'].to_numpy()
#    print(len(close))
#    ts_mean3 = ti.sma(close, period=3)

#    print(len(ts_mean3))


#    query = cur.execute("SELECT exchange, symbol, period, time, open, high, low, close, volume FROM candlesticks")
    
#    cols = [column[0] for column in query.description]
    
#    rows = cur.fetchall()

#    results= pd.DataFrame.from_records(data = rows, columns = cols)

#    print(results.head(5))

def candlesticks_to_pd(rows):
    cols = ['exchange', 'symbol', 'period', 'time', 'open', 'high', 'low', 'close', 'volume']
    return pd.DataFrame.from_records(data = rows, columns = cols)


if __name__ == '__main__':
    #iii = Instance()
    #s = zerorpc.Server(RpcBridge(iii))
    #s.bind("tcp://0.0.0.0:4242")
    #s.run()


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