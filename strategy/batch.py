from strategy.strategy import AbstractStrategy
from strategy.alpha import Alpha

# could be a subclass of strategy, where each alpha in strategy has equal weights
class Batch(AbstractStrategy):

    def __init__(self, alphas, ticker=None):
        self.weighted = {}

        assert isinstance(alphas, list)
        assert len(alphas) > 0

        w = 1 / len(alphas)

        data_manager = alphas[0].get_main_data_manager()

        for alpha in alphas:
            assert isinstance(alpha,Alpha)
            self.weighted[alpha] = w

        super().__init__(data_manager, self.weighted, ticker=ticker)