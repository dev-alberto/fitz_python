from datetime import datetime

def get_datetime_from_miliseconds(miliseconds):
    return datetime.fromtimestamp(miliseconds / 1000.0)