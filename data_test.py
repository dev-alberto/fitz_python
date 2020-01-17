from db_connect import Connect
from data_retriever import *
from datetime import datetime

if __name__ == '__main__':
    
    conn = Connect('binance_0.1.db')

    conn2 = Connect('fitz.db')

    cur = conn.cursor()

    cur2 = conn2.cursor()

    symbol = 'BTCUSDT'
    period = '1m'
    exchange = 'binance'

    dt = datetime(2019, 10, 10, hour=17, minute=6, second=0).replace(tzinfo=timezone.utc)

    # print(int(dt.replace(tzinfo=timezone.utc).timestamp()))

    # print(int(time.mktime(dt.timetuple())*1e3 + dt.microsecond/1e3))

    # data1 = Get_candlesticks_between_dates(cur, "2019-7-12-17-0-0", "2019-7-16-18-0-0", period,symbol,exchange)

    # data2 = Get_all_candlesticks_with_period(cur2, period, symbol, exchange)

    # start = Get_datetime_from_miliseconds(data2[0]['time'])
    # end = Get_datetime_from_miliseconds(data2[-1]['time'])
    # print(start, end)

    #dd = Get_all_gecko_data(cur, symbol, 1)

    #start = Get_datetime_from_miliseconds(dd[0]['time'])
    #end = Get_datetime_from_miliseconds(dd[-1]['time'])

    # print(dd[-1]['close'])

    #print(len(dd))

    #print(start, end)

    #print(len(dd))


