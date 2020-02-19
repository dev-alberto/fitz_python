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
    return datetime.utcfromtimestamp(ms//1000).replace(microsecond=ms % 1000*1000)


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


# SELECT time as 'start', close, high, low, open, volumefrom as 'volume'
#  from aggregate WHERE from_currency='BTC' and to_currency='USD' ORDER BY time ASC
def format_cata_data(rows):
    assert len(rows) > 0

    res = []

    for r in rows:
        d = {}
        tt = int(r[0])

        # gherla
        if tt < 1562198400:
            continue
        d['exchange'] = 'binance'
        d['symbol'] = 'BTCUSDT'
        d['period'] = '1m'
        d['time'] = tt
        d['open'] = r[4]
        d['high'] = r[2]
        d['low'] = r[3]
        d['close'] = r[1]
        d['volume'] = r[5]
        res.append(d)

    return res


def format_gecko_data(rows, symbol):
    assert len(rows) > 0

    res = []
    prev_time = int(rows[0][0]) #* 1000
    for r in rows:
        d = {}
        d['exchange'] = 'binance'
        d['symbol'] = symbol
        d['period'] = '1m'
        d['time'] = int(r[0])# * 1000
        d['open'] = r[1]
        d['high'] = r[2]
        d['low'] = r[3]
        d['close'] = r[4]
        d['volume'] = r[5]

        if prev_time > d['time']:
            break

        prev_time = d['time']
        res.append(d)
    #print(res)
    #for ii in range(len(res) - 1):
        # check consecutive time stamps ...
    #    assert res[ii + 1]['time'] - res[ii]['time'] == 60000

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
    s3 = " period='" + period + "' and "

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


def Get_all_gecko_data(cursor, symbol, period):
    qq = "select start, open, high, low, close, volume FROM candles_USDT_BTC order by start asc"

    cursor.execute(qq)

    data = format_gecko_data(cursor.fetchall(), symbol)
    return Resample_gecko_data(data, period, symbol)


def Get_all_cata_data(cursor, symbol, period):
    qq = "SELECT time as 'start', close, high, low, open, volumefrom as 'volume' " \
         "from aggregate WHERE from_currency='BTC' and to_currency='USD' ORDER BY time ASC"

    cursor.execute(qq)

    data = format_cata_data(cursor.fetchall())

    return Resample_gecko_data(data, period, symbol)


def Get_gecko_between_dates(cursor, symbol, period, date1, date2):
    d1 = date1.split('-')
    d2 = date2.split('-')
    assert len(d1) == 6
    assert len(d2) == 6

    u_d1 = get_unix_time_miliseconds(int(d1[0]), int(d1[1]), int(d1[2]), int(d1[3]), int(d1[4]), int(d1[5])) // 1000
    u_d2 = get_unix_time_miliseconds(int(d2[0]), int(d2[1]), int(d2[2]), int(d2[3]), int(d2[4]), int(d2[5])) // 1000

    qq = "select start, open, high, low, close, volume FROM candles_USDT_BTC where "

    s4 = " start between " + str(u_d1) + " and " + str(u_d2)
    qq += s4

    cursor.execute(qq)

    data = format_gecko_data(cursor.fetchall(), symbol)

    return Resample_gecko_data(data, period, symbol)


# this should provide the data in 5m, 15m etc form. It should be in the same format as data,
# as to be compatible with our platform
def Resample_gecko_data(data, period, symbol):
    ll = len(data)
    res = []
    if period == 1:
        return data

    for idx in range(1, ll):
        if (idx + 1) % period == 0:
            candle = {}
            start_idx = idx + 1 - period
            ii = data[start_idx]['time']
            close = data[idx]['close']
            open_ = data[start_idx]['open']
            volume = 0
            low = data[start_idx]['low']
            high = data[start_idx]['high']
            for i in range(start_idx, idx+1):
                volume += data[i]['volume']
                if data[i]['low'] < low:
                    low = data[i]['low']
                if data[i]['high'] > high:
                    high = data[i]['high']

            candle['time'] = ii
            candle['close'] = close
            candle['high'] = high
            candle['low'] = low
            candle['open'] = open_
            candle['volume'] = volume
            candle['exchange'] = 'binance'
            candle['symbol'] = symbol
            pp = str(period) + 'm'
            if period == 60:
                pp = '1h'
            if period == 120:
                pp = '2h'
            elif period == 240:
                pp = '4h'
            elif period == 360:
                pp = '6h'
            elif period == 720:
                pp = '12h'
            elif period == 1440:
                pp = '1d'
            elif period == 10080:
                pp = '1w'

            candle['period'] = pp
            res.append(candle)

    return res
