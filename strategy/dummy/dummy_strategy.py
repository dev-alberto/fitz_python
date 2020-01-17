from strategy.strategy import AbstractStrategy
from strategy.dummy.dummy_alpha import DumbAlpha
from feature.close import Close
from feature.high import High
from feature.low import Low
from feature.open import Open


class DumbStrategy(AbstractStrategy):

    def __init__(self, raw_data_manager1min, raw_data_manager5min, raw_data_manager1h, raw_data_manager4h, ticker=None):

        clsm = Close(raw_data_manager1min)
        openm = Open(raw_data_manager1min)

        cls5 = Close(raw_data_manager5min)
        hi1 = High(raw_data_manager1h)
        low1 = Low(raw_data_manager1h)
        cls1 = Close(raw_data_manager1h)
        opn1 = Open(raw_data_manager1h)
        open5 = Open(raw_data_manager5min)

        hi4 = High(raw_data_manager4h)
        low4 = Low(raw_data_manager4h)
        cls4 = Close(raw_data_manager4h)
        opn4 = Open(raw_data_manager4h)

        #dumb_alpha = DumbAlpha(cls5, cls1, opn1, hi1, low1, raw_data_manager1min)
        dumb_alpha = DumbAlpha(clsm, openm, cls5, cls1, opn1, hi1, low1, open5, raw_data_manager1min)

        weights = {dumb_alpha: 1}

        super().__init__(raw_data_manager1min, weights, ticker=ticker)
