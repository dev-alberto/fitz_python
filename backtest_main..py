from db_connect import Connect
from rpc.rpc_bridge import RpcBridge
from rpc.db_bridge import DbBridge
from instance import Instance

from strategy.random import RandomBTCUSDT
from strategy.simple_reversion import Min_Max_Normalized_Returns_Reversion
from strategy.bollinger.boll1 import BollingerImpl1
from strategy.backtest import Backtest

from feature.mean_returns import MeanReturns
from feature.returns import Returns
from feature.cross_cbl import Cross_cBL
from feature.cross_bhc import Cross_BHc

from feature.bollinger_low import BollingerLow
from feature.bollinger_high import BollingerHigh

from data_retriever import Get_all_candles, Get_candlesticks_between_dates

    #r = Returns(5800, btc1min)

    #r.backfill()

    #mean_r = MeanReturns(5, btc1min, r)

    #mean_r.backfill()

    #mean_s = Min_Max_Normalized_Returns_Reversion(mean_r, btc1min)

if __name__ == '__main__':
    
    conn = Connect('fitz.db')
    cur = conn.cursor()

    symbol = 'BTCUSDT'
    period = '1m'
    exchange = 'binance'

    data = Get_candlesticks_between_dates(cur, "2019-7-12-17-0-0", "2019-7-16-18-0-0", period,symbol,exchange)
    
    js = {'symbols': [{'symbol': symbol, 'periods': ['1m'], 'exchange': 'binance', 'state': 'watch', 'history': len(data),'strategies': []}]}

    ii = Instance()
    
    db_bridge = DbBridge(ii)
    db_bridge.instantiate(js)

    db_bridge.backfill(exchange, symbol, period, data)

    raw_data_managers = ii.get_raw_data_managers()

    btc1min = raw_data_managers['binanceBTCUSDT1m']

    bl = BollingerLow(90, 3, btc1min)
    bl.backfill()

    bh = BollingerHigh(90, 3, btc1min)
    bh.backfill()
    

    cross_cbl = Cross_cBL(bl, btc1min)
    cross_cbl.backfill()

    cross_bhc = Cross_BHc(bh, btc1min)
    cross_bhc.backfill()


    boll1 = BollingerImpl1(cross_cbl, cross_bhc, btc1min)


    backtest = Backtest('2019-7-12-17-0-0',boll1, 0.075)

    ll = backtest.compute_pnl()

    print(sum(ll['returns']))

    print(ll.head(10))