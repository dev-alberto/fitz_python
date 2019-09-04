from strategy.strategy import AbstractStrategy
#from feature.bollinger_high import BollingerHigh
#from feature.bollinger_low import BollingerLow
#from feature.bollinger_middle import BollingerMiddle


class BollingerS(AbstractStrategy):

    def __init__(self, raw_data_manager, cross_cbl=None, cross_blc=None, cross_cbm=None, 
    cross_bmc=None,cross_cbh=None, cross_bhc=None, is_live=False):
        
        f_list = []

        if cross_cbl is not None:
            f_list.append(cross_cbl)

        if cross_blc is not None:
            f_list.append(cross_blc)

        if cross_cbm is not None:
            f_list.append(cross_cbm)

        if cross_bmc is not None:
            f_list.append(cross_bmc)
        
        if cross_cbh is not None:
            f_list.append(cross_cbh)

        if cross_bhc is not None:
            f_list.append(cross_bhc)
        
        super().__init__(initial_allocation=0, pair='BTCUSDT', period='1m', raw_data_managers=[raw_data_manager], 
                        feature_list=f_list, model=None,is_live=is_live)

    def compute(self, ii, feature_val):
        if feature_val == 1:
            self.allocation = 1
        else:
            self.allocation = 0
        
        return self.allocation
       
       # if self.allocation < 1:
       #     if feature_val > 0:
       #         feature_val = 1
       #     else: feature_val = 0
        
       # if self.allocation == 1:
       #     if feature_val < 0:
       #         feature_val = 0
       #     else: feature_val = 1
        
       # self.allocation = feature_val
      #  return self.allocation
       
        