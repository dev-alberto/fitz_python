from datetime import datetime, timedelta


def get_datetime_from_miliseconds(miliseconds):
    return datetime.fromtimestamp(miliseconds / 1000.0)


# does not work
def roundTime(dt=None, roundTo=60):
    if dt == None:
       dt = datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + timedelta(0,rounding-seconds, -dt.microsecond)
