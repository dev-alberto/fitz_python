from feature.feature import EmptyFeature
from feature.returns import Returns
import tulipy as ti


class MeanReturns(EmptyFeature):

    def __init__(self, lookback, raw_data_manager, returns):
        assert isinstance(returns, Returns)
        assert returns.get_history_length() > lookback
        self.returns = returns
        super().__init__(lookback, raw_data_manager,history_lengh=returns.get_history_length() - lookback, features=[returns])

    def compute(self, data_dict):

        returns = self.returns.get_numpy()

        return ti.sma(returns, self.lookback)
