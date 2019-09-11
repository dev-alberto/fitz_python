from strategy.bollinger.bollinger_alpha import BollApha

# -up + down + sup
class BollingerImpl2(BollApha):

    def __init__(self, cross_cbl, cross_bhc, cross_cbh, raw_data_manager):
        self.cross_bhc = cross_bhc
        self.cross_cbl = cross_cbl
        self.cross_cbh = cross_cbh
        
        super().__init__(raw_data_manager, cross_cbl=cross_cbl, cross_bhc=cross_bhc,cross_cbh=cross_cbh)

    def compute(self, ii):
        #val = - self.cross_cbl[ii] + self.cross_bhc[ii]
        
        val = - self.cross_cbl[ii] + self.cross_bhc[ii] + self.cross_cbh[ii]

        return super().compute(ii, val)
