from db_connect import Connect
from data_retriever import *
from datetime import datetime

if __name__ == '__main__':
    
    conn = Connect('binance_0.1.db')

    conn2 = Connect('fitz.db')

    conn3 = Connect('data.db')

    cur = conn3.cursor()

    symbol = 'BTCUSDT'
    period = '1m'
    exchange = 'binance'

    data3 = Get_all_cata_data(cur, symbol, 5)


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


