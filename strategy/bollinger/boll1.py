from strategy.bollinger.bollinger_alpha import BollApha


# -up + down
class BollingerImpl1(BollApha):

    def __init__(self, cross_cbl, cross_bhc):
        self.cross_bhc = cross_bhc
        self.cross_cbl = cross_cbl
        
        super().__init__(cross_cbl=cross_cbl, cross_bhc=cross_bhc)

    def compute(self, ii):
        # val = - self.cross_cbl[ii] + self.cross_bhc[ii]
        
        val = - self.cross_cbl[ii] + self.cross_bhc[ii]

        return super().compute_(val)
