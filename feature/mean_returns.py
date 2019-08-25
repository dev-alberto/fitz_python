from feature.feature import EmptyFeature
from feature.returns import Returns
import tulipy as ti

class MeanReturns(EmptyFeature):

    def __init__(self, lookback, raw_data_manager, returns):
        assert isinstance(returns, Returns)
        assert returns.get_history_length() > lookback
        super().__init__(returns.get_history_length() - lookback, lookback, raw_data_manager, features=[returns])
        self.returns = returns

    def compute(self, data_dict):

        returns = self.returns.get_feature()

        return ti.sma(returns, self.lookback)