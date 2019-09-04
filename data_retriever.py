from datetime import datetime, timezone
import time

def get_unix_time_miliseconds(yy, MM, dd, hh, mm, ss):
    dt = datetime(yy, MM, dd, hour=hh, minute=mm, second=ss).replace(tzinfo=timezone.utc)
    return int(time.mktime(dt.timetuple())*1e3 + dt.microsecond/1e3)

def Parse_string_date(date):
    d = date.split('-')
    
    assert len(d) == 6

    return datetime(int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]), int(d[5]))

def Get_datetime_from_miliseconds(ms):
    return datetime.utcfromtimestamp(ms//1000).replace(microsecond=ms%1000*1000)


def Get_all_candles(cursor):
    cursor.execute("SELECT exchange, symbol, period, time, open, high, low, close, volume FROM candlesticks")    
    return cursor.fetchall()

# data will be formated to match a list of dicts, where each dict is a row entry 
def format_data(rows):
    assert len(rows) > 0

    res = []
    for r in rows:
        d = {}
        d['exchange'] = r[0]
        d['symbol'] = r[1]
        d['period'] = r[2]
        d['time'] = r[3]
        d['open'] = r[4]
        d['high'] = r[5]
        d['low'] = r[6]
        d['close'] = r[7]
        d['volume'] = r[8]
        res.append(d)

    return res

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
    return format_data(cursor.fetchall())

def Get_all_candlesticks_with_period(cursor, period, symbol, exchange):
    qq = "select exchange, symbol, period, time, open, high, low, close, volume FROM candlesticks where "
    s1 = " exchange='" + exchange  + "' and "
    s2 = " symbol='" + symbol + "' and "
    s3  = " period='" + period + "' "

    qq += s1 + s2 + s3

    cursor.execute(qq)
    return format_data(cursor.fetchall())