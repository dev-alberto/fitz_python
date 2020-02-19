from data.db_connect import Connect
from rpc.db_bridge import DbBridge
from instance import Instance

import pandas as pd

from data.data_retriever import *
from feature.feature import EmptyFeature

from feature.adosc import Adosc
# from feature.adxr import Adxr
from feature.aroonosc import Aroonosc
from feature.atr import Atr
from feature.bop import Bop
from feature.cvi import Cvi
from feature.dpo import Dpo
from feature.dx import Dx
from feature.ad import Ad
from feature.kvo import Kvo
from feature.linregslope import LinRegSlope
from feature.mfi import Mfi
from feature.nvi import Nvi
from feature.pvi import Pvi
from feature.bollingerhigh import BollingerHigh
from feature.bollingermiddle import BollingerMiddle
from feature.bollingerlow import BollingerLow
from feature.returns import Returns
from feature.ema import Ema
from feature.sma import Sma
from feature.stochrsid import StochRsiD
from feature.stochrsih import StochRsiH
from feature.rsi import Rsi
from feature.vwap import Vwap


def add_column_to_pandas(dataF, ff, args=None):
    assert isinstance(args, list)
    assert isinstance(ff, EmptyFeature)

    name = '_'.join([str(i) for i in args])
    dataF[name] = ff.get_TS()
    return dataF


if __name__ == '__main__':
    pass
