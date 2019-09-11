from strategy.bollinger.bollinger_alpha import BollApha

# -up + down - sup + sdown - mup + mdown
class BollingerImpl4(BollApha):

    def __init__(self, cross_cbl, cross_bhc, cross_cbh, cross_blc, cross_bmc, cross_cbm, raw_data_manager):
        
        self.cross_bhc = cross_bhc
        self.cross_cbl = cross_cbl
        self.cross_cbh = cross_cbh
        self.cross_blc = cross_blc
        self.cross_bmc = cross_bmc
        self.cross_cbm = cross_cbm
        
        super().__init__(raw_data_manager, cross_cbl=cross_cbl, cross_bhc=cross_bhc,cross_cbh=cross_cbh,cross_blc=cross_blc,cross_bmc=cross_bmc,cross_cbm=cross_cbm)

    def compute(self, ii):
        #val = - self.cross_cbl[ii] + self.cross_bhc[ii]
        
        val = - self.cross_cbl[ii] + self.cross_bhc[ii] - self.cross_cbh[ii] + self.cross_blc[ii] - self.cross_cbm[ii] + self.cross_bmc[ii]

        return super().compute(ii, val)
