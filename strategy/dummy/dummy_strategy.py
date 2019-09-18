from strategy.strategy import AbstractStrategy
from strategy.dummy.dummy_alpha import DumbAlpha
from feature.close import Close


class DumbStrategy(AbstractStrategy):

    def __init__(self, raw_data_manager1min, raw_data_manager5min, ticker=None):

        cls1 = Close(raw_data_manager1min)
        cls5 = Close(raw_data_manager5min)

        dumb_alpha = DumbAlpha(cls1, cls5, raw_data_manager1min)

        weights = {dumb_alpha: 1}

        super().__init__(raw_data_manager1min, weights, ticker=ticker)
