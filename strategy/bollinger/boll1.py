from strategy.bollinger.bollingerS import BollingerS

# -up + down
class BollingerImpl1(BollingerS):

    def __init__(self, cross_cbl, cross_bhc, raw_data_manager, is_live=False):
        super().__init__(raw_data_manager,cross_cbl=cross_cbl,cross_bhc=cross_bhc,is_live=is_live)

        self.cross_bhc = cross_bhc
        self.cross_cbl = cross_cbl

        self.cross_cbl_ts = cross_cbl.get_TS()
        self.cross_bhc_ts = cross_bhc.get_TS()

    def compute(self, ii):
        #val = - self.cross_cbl[ii] + self.cross_bhc[ii]
        val = 0
        print(ii)
        if self.is_live:
            cbl = self.cross_cbl.get_latest()
            bhc = self.cross_bhc.get_latest()
            val = - cbl + bhc

        else: val = - self.cross_cbl_ts[ii] + self.cross_bhc_ts[ii]

        return super().compute(ii, val)
