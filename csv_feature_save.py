from db_connect import Connect
from rpc.rpc_bridge import RpcBridge
from rpc.db_bridge import DbBridge
from instance import Instance

import pandas as pd

from data_retriever import *
from feature.feature import EmptyFeature

from feature.ad import Ad
from feature.adosc import Adosc
# from feature.adxr import Adxr
from feature.aroonosc import Aroonosc
from feature.atr import Atr
from feature.bop import Bop
from feature.cmo import Cmo
from feature.cvi import Cvi
from feature.dpo import Dpo
from feature.dx import Dx
from feature.ad import Ad
from feature.kvo import Kvo
from feature.linregslope import LinRegSlope
from feature.mfi import Mfi
from feature.nvi import Nvi
from feature.pvi import Pvi
from feature.close import Close
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
from feature.crossbhc import CrossBHc
from feature.crossbmc import CrossBmc
from feature.crossblc import CrossBLc


def add_column_to_pandas(dataF, ff, args=None):
    assert isinstance(args, list)
    assert isinstance(ff, EmptyFeature)

    name = '_'.join([str(i) for i in args])
    dataF[name] = ff.get_TS()
    return dataF


if __name__ == '__main__':
    # conn = Connect('fitz.db')
    # conn = Connect('binance_0.1.db')

    conn = Connect('data.db')

    cur = conn.cursor()

    symbol = 'BTCUSDT'
    periods = ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '6h', '12h']
    exchange = 'binance'

    data1min = Get_all_cata_data(cur, symbol, 1)
    data3min = Get_all_cata_data(cur, symbol, 3)
    data5min = Get_all_cata_data(cur, symbol, 5)
    data15min = Get_all_cata_data(cur, symbol, 15)
    data30min = Get_all_cata_data(cur, symbol, 30)
    data1h = Get_all_cata_data(cur, symbol, 60)
    data4h = Get_all_cata_data(cur, symbol, 240)
    data6h = Get_all_cata_data(cur, symbol, 360)
    data12h = Get_all_cata_data(cur, symbol, 720)

    # data1min = Get_all_gecko_data(cur, symbol, 1)
    # data3min = Get_all_gecko_data(cur, symbol, 3)
    # data5min = Get_all_gecko_data(cur, symbol, 5)
    # data15min = Get_all_gecko_data(cur, symbol, 15)
    # data30min = Get_all_gecko_data(cur, symbol, 30)
    # data1h = Get_all_gecko_data(cur, symbol, 60)
    # data4h = Get_all_gecko_data(cur, symbol, 240)
    # data6h = Get_all_gecko_data(cur, symbol, 360)
    # data12h = Get_all_gecko_data(cur, symbol, 720)

    js = {'symbols': [{'symbol': symbol, 'periods': periods, 'exchange': 'binance', 'state': 'watch',
                       'history': len(data1min), 'strategies': []}]}

    ii = Instance()

    db_bridge = DbBridge(ii)
    db_bridge.instantiate(js)

    db_bridge.backfill(exchange, symbol, '1m', data1min)
    db_bridge.backfill(exchange, symbol, '3m', data3min)
    db_bridge.backfill(exchange, symbol, '5m', data5min)
    db_bridge.backfill(exchange, symbol, '15m', data15min)
    db_bridge.backfill(exchange, symbol, '30m', data30min)
    db_bridge.backfill(exchange, symbol, '1h', data1h)
    db_bridge.backfill(exchange, symbol, '4h', data4h)
    db_bridge.backfill(exchange, symbol, '6h', data6h)
    db_bridge.backfill(exchange, symbol, '12h', data12h)

    raw_data_managers = ii.get_raw_data_managers()

    btc1min = raw_data_managers['binanceBTCUSDT1m']

    btc3min = raw_data_managers['binanceBTCUSDT3m']

    btc5min = raw_data_managers['binanceBTCUSDT5m']

    btc15min = raw_data_managers['binanceBTCUSDT15m']

    btc30min = raw_data_managers['binanceBTCUSDT30m']

    btc1h = raw_data_managers['binanceBTCUSDT1h']

    btc4h = raw_data_managers['binanceBTCUSDT4h']
    btc6h = raw_data_managers['binanceBTCUSDT6h']

    btc12h = raw_data_managers['binanceBTCUSDT12h']

    managers = [btc1min, btc3min, btc5min, btc15min, btc30min, btc1h, btc4h, btc6h, btc12h]


    all_pandas = {}
    for manager in managers:

        pp = manager.get_backfill_df()
        per = manager.get_period()
        assert isinstance(pp, pd.DataFrame)

        ret = Returns(manager)
        pp = add_column_to_pandas(pp, ret, [type(ret).__name__, per])

        ad = Ad(manager)
        pp = add_column_to_pandas(pp, ad, [type(ad).__name__, per])

        nvi = Nvi(manager)
        pp = add_column_to_pandas(pp, nvi, [type(nvi).__name__, per])

        pvi = Pvi(manager)
        pp = add_column_to_pandas(pp, pvi, [type(pvi).__name__, per])

        bop = Bop(manager)
        pp = add_column_to_pandas(pp, bop, [type(bop).__name__, per])

        sma_lookbacks = [10, 30, 50, 100, 200]
        ema_lookbacks = [21, 55, 100, 200, 300]
        rsi_lookbacks = [14, 21, 60]
        stoch_rsi = [(5, 3, 3), (21, 14, 14), (14, 3, 3)]
        adosc_params = [(2, 5), (3, 5), (3, 10), (5, 14), (14, 21)]
        aroon_params = [5, 10, 14, 21]
        atr_params = [5, 10, 14, 21]
        bollinger_params = [(14, 2), (20, 2), (50, 2), (14, 2.5), (20, 2.5), (50, 2.5), (14, 3), (20, 3), (50, 3)]
        cvi_params = [5, 10, 20, 50, 100]
        dpo_params = [5, 10, 20, 50]
        dx_params = [5, 14, 20, 50, 100, 200]
        kvo_params = [(2, 5), (3, 10), (5, 14), (14, 21)]
        lin_reg_slope = [5, 14, 20, 50, 100]
        mfi_params = [14, 21, 60]
        vwap_params = [5, 14, 20, 50, 100]

        for i in sma_lookbacks:
            sma = Sma(i, manager)
            pp = add_column_to_pandas(pp, sma, [type(sma).__name__, per, i])

        for i in ema_lookbacks:
            ema = Ema(i, manager)
            pp = add_column_to_pandas(pp, ema, [type(ema).__name__, per, i])

        for i in rsi_lookbacks:
            rsi = Rsi(i, manager)
            pp = add_column_to_pandas(pp, rsi, [type(rsi).__name__, per, i])

        for i in aroon_params:
            aroon = Aroonosc(i, manager)
            pp = add_column_to_pandas(pp, aroon, [type(aroon).__name__, per, i])

        for i in atr_params:
            atr = Atr(i, manager)
            pp = add_column_to_pandas(pp, atr, [type(atr).__name__, per, i])

        for i in dpo_params:
            dpo = Dpo(i, manager)
            pp = add_column_to_pandas(pp, dpo, [type(dpo).__name__, per, i])

        for i in cvi_params:
            cvi = Cvi(i, manager)
            pp = add_column_to_pandas(pp, cvi, [type(cvi).__name__, per, i])

        for i in dx_params:
            dx = Dx(i, manager)
            pp = add_column_to_pandas(pp, dx, [type(dx).__name__, per, i])

        for i in lin_reg_slope:
            llin = LinRegSlope(i, manager)
            pp = add_column_to_pandas(pp, llin, [type(llin).__name__, per, i])

        for i in mfi_params:
            mfi = Mfi(i, manager)
            pp = add_column_to_pandas(pp, mfi, [type(mfi).__name__, per, i])

        for i in vwap_params:
            vwap = Vwap(i, manager)
            pp = add_column_to_pandas(pp, vwap, [type(vwap).__name__, per, i])

        for i in adosc_params:
            adoosc = Adosc(i[0], i[1], manager)
            pp = add_column_to_pandas(pp, adoosc, [type(adoosc).__name__, per, i[0], i[1]])

        for i in kvo_params:
            kvo = Kvo(i[0], i[1], manager)
            pp = add_column_to_pandas(pp, kvo, [type(kvo).__name__, per, i[0], i[1]])

        for i in bollinger_params:
            bh = BollingerHigh(i[0], i[1], manager)
            bm = BollingerMiddle(i[0], i[1], manager)
            bl = BollingerLow(i[0], i[1], manager)

            pp = add_column_to_pandas(pp, bh, [type(bh).__name__, per, i[0], i[1]])
            pp = add_column_to_pandas(pp, bm, [type(bm).__name__, per, i[0], i[1]])
            pp = add_column_to_pandas(pp, bl, [type(bl).__name__, per, i[0], i[1]])

        for i in stoch_rsi:
            stochd = StochRsiD(i[0], i[1], i[2], manager)
            stochh = StochRsiH(i[0], i[1], i[2], manager)
            pp = add_column_to_pandas(pp, stochd, [type(stochd).__name__, per, i[0], i[1], i[2]])
            pp = add_column_to_pandas(pp, stochh, [type(stochh).__name__, per, i[0], i[1], i[2]])

        all_pandas[manager.get_period()] = pp

    for k, v in all_pandas.items():
        path = 'data_test/features/cata' + k + '.csv'
        assert isinstance(v, pd.DataFrame)
        v.to_csv(path, index_label='time')



    # bol_batch = BollingerBatch(btc1min)

    # backtest.save_to_disk()

