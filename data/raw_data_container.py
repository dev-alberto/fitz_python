

# contains raw queue structures for price data
class Raw:
    def __init__(self, time=None, open=None, high=None, low=None, close=None, volume=None):

        self.d = {}
    
    def set_time(self, time):
        #self.time = time
        self.d['time'] = time

    def set_open(self, open):
        #self.open = open
        self.d['open'] = open


    def set_high(self, high):
        #self.high = high
        self.d['high'] = high

    def set_low(self, low):
        #self.low = low
        self.d['low'] = low

    def set_close(self, close):
        #self.close = close
        self.d['close'] = close

    def set_volume(self, volume):
        #self.volume = volume
        self.d['volume'] = volume
    

    def update_time(self, v):
        #return self.time
        if self.d.get('time') != None:
            self.d['time'].append(v)

    def update_open(self, v):
        if self.d.get('open') != None:
            self.d['open'].append(v)

    def update_high(self, v):
        if self.d.get('high') != None:
            self.d['high'].append(v)

    def update_low(self, v):
        if self.d.get('low') != None:
            self.d['low'].append(v)

    def update_close(self, v):
        if self.d.get('close') != None:
            self.d['close'].append(v)

    def update_volume(self, v):
        if self.d.get('volume') != None:
            self.d['volume'].append(v)

    def get_data(self):
        return self.d
