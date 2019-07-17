from datetime import datetime, timezone
import time

def get_unix_time_miliseconds(yy, MM, dd, hh, mm, ss):
    dt = datetime(yy, MM, dd, hour=hh, minute=mm, second=ss).replace(tzinfo=timezone.utc)
    return int(time.mktime(dt.timetuple())*1e3 + dt.microsecond/1e3)


def Get_all_candles(cursor):
    cursor.execute("SELECT exchange, symbol, period, time, open, high, low, close, volume FROM candlesticks")    
    return cursor.fetchall()


# input dates like YYYY-MM-DD-HH-MM-SS (for example 2019-7-16-17-0-0)
def Get_candlesticks_between_dates(cursor, date1, date2, period, symbol, exchange):
    d1 = date1.split('-')
    d2 = date2.split('-')
    assert len(d1) == 6
    assert len(d2) == 6

    u_d1 = get_unix_time_miliseconds(int(d1[0]), int(d1[1]), int(d1[2]), int(d1[3]), int(d1[4]), int(d1[5]))
    u_d2 = get_unix_time_miliseconds(int(d2[0]), int(d2[1]), int(d2[2]), int(d2[3]), int(d2[4]), int(d2[5]))

    qq = "select exchange, symbol, period, time, open, high, low, close, volume FROM candlesticks where "
    s1 = " exchange='" + exchange  + "' and "
    s2 = " symbol='" + symbol + "' and "
    s3  = " period='" + period + "' and "

    s4 = " time between " + str(u_d1) + " and " + str(u_d2)
    qq += s1 + s2 + s3 + s4

    cursor.execute(qq)
    return cursor.fetchall()