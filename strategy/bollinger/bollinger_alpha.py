from strategy.alpha import Alpha


class BollApha(Alpha):
    def __init__(self, cross_cbl=None, cross_blc=None, cross_cbm=None,
                 cross_bmc=None, cross_cbh=None, cross_bhc=None):

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

        super().__init__(feature_list=f_list, model=None, init_alloc=0)

    def compute_(self, feature_val):

        if self.allocation < 1:
            if feature_val > 0:
                self.allocation = 1
            else:
                self.allocation = 0

        if self.allocation == 1:
            if feature_val < 0:
                self.allocation = 0

            else:
                self.allocation = 1

        return self.allocation
