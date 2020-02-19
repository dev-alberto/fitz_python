from numpy_ringbuffer import RingBuffer

class Ticker:

    def __init__(self, lookback, exchange, symbol, bid, ask, updated_at):
        
        self.exchange = exchange
        self.symbol = symbol
        self.bid = bid 
        self.ask = ask
        self.updated_at = updated_at

        self.bid_lookback = RingBuffer(capacity=lookback, dtype=object)
        self.ask_lookback = RingBuffer(capacity=lookback, dtype=object)


    def get_bid(self):
        return self.bid

    def get_ask(self):
        return self.ask

    def get_time(self):
        return self.updated_at

    def update(self, data):
        
        self.bid = data['bid']
        self.ask = data['ask']

        self.updated_at = data['time']

        self.bid_lookback.append(self.bid)
        self.ask_lookback.append(self.ask)
