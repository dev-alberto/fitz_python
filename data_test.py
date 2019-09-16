from db_connect import Connect
from data_retriever import *


if __name__ == '__main__':
    
    conn = Connect('binance_0.1.db')

    conn2 = Connect('fitz.db')

    cur = conn.cursor()

    cur2 = conn2.cursor()

    symbol = 'BTCUSDT'
    period = '1m'
    exchange = 'binance'

    # data1 = Get_candlesticks_between_dates(cur, "2019-7-12-17-0-0", "2019-7-16-18-0-0", period,symbol,exchange)

    # data2 = Get_all_candlesticks_with_period(cur2, period, symbol, exchange)

    # start = Get_datetime_from_miliseconds(data2[0]['time'])
    # end = Get_datetime_from_miliseconds(data2[-1]['time'])
    # print(start, end)

    # dd = Get_all_gecko_data(cur, symbol)
    #
    # start = Get_datetime_from_miliseconds(dd[0]['time'])
    # end = Get_datetime_from_miliseconds(dd[-1]['time'])
    #
    # print(dd[-1]['close'])
    #
    # print(start, end)

    dd = Get_gecko_between_dates(cur, symbol, "2019-1-15-0-0-0", "2019-1-16-0-0-0")

    print(len(dd))


