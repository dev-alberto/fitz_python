from strategy.bollinger.bollingerS import BollingerS

# -up + down
class BollingerImpl1(BollingerS):

    def __init__(self, cross_cbl, cross_bhc, raw_data_manager):
        super().__init__(raw_data_manager,cross_cbl=cross_cbl,cross_bhc=cross_bhc)

        self.cross_cbl = cross_cbl.get_TS()
        self.cross_bhc = cross_bhc.get_TS()

    def compute(self, ii):
        val = - self.cross_cbl[ii] + self.cross_bhc[ii]
        return super().compute(ii, val)
