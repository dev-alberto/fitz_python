from db_connect import Connect
from rpc.rpc_bridge import RpcBridge
from rpc.db_bridge import DbBridge
from instance import Instance


from strategy.bollinger.boll2 import BollingerImpl2
from strategy.bollinger.bollinger_strategy import BollingerStrategy
from strategy.bollinger.bollinger_batch import BollingerBatch

from feature.LogReturns import LogReturns
from strategy.returns.returns import Returns0
from strategy.dummy.dummy_strategy import DumbStrategy

from strategy.backtest.simulator import Simulator

from data_retriever import *


from feature.LogReturns import LogReturns


if __name__ == '__main__':
    
    # conn = Connect('fitz.db')
    conn = Connect('binance_0.1.db')

    cur = conn.cursor()

    symbol = 'BTCUSDT'
    periods = ['1m', '5m', '15m', '30m', '1h', '4h']
    exchange = 'binance'

    # data = Get_candlesticks_between_dates(cur, "2019-7-12-17-0-0", "2019-7-16-18-0-0", period,symbol,exchange)
    # data = Get_all_candlesticks_with_period(cur, period,symbol,exchange)

    #data1min = Get_all_gecko_data(cur, symbol, 1)
    #data5min = Get_all_gecko_data(cur, symbol, 5)

    #data1min = Get_gecko_between_dates(cur, symbol, 1, "2019-1-12-0-0-0", "2019-5-12-0-0-0")
    #data5min = Get_gecko_between_dates(cur, symbol, 5, "2019-1-12-0-0-0", "2019-5-12-0-0-0")
    #data1h = Get_gecko_between_dates(cur, symbol, 60, "2019-1-12-0-0-0", "2019-5-12-0-0-0")
    #data4h = Get_gecko_between_dates(cur, symbol, 240, "2019-1-12-0-0-0", "2019-5-12-0-0-0")

    data1min = Get_all_gecko_data(cur, symbol, 1)
    data5min = Get_all_gecko_data(cur, symbol, 5)
    data15min = Get_all_gecko_data(cur, symbol, 15)
    data30min = Get_all_gecko_data(cur, symbol, 30)
    data1h = Get_all_gecko_data(cur, symbol, 60)
    data4h = Get_all_gecko_data(cur, symbol, 240)


    js = {'symbols': [{'symbol': symbol, 'periods': periods, 'exchange': 'binance', 'state': 'watch',
                       'history': len(data1min), 'strategies': []}]}

    ii = Instance()
    
    db_bridge = DbBridge(ii)
    db_bridge.instantiate(js)

    db_bridge.backfill(exchange, symbol, '1m', data1min)
    db_bridge.backfill(exchange, symbol, '5m', data5min)
    db_bridge.backfill(exchange, symbol, '15m', data15min)
    db_bridge.backfill(exchange, symbol, '30m', data30min)
    db_bridge.backfill(exchange, symbol, '1h', data1h)
    db_bridge.backfill(exchange, symbol, '4h', data4h)


    raw_data_managers = ii.get_raw_data_managers()

    print("************")
    print(raw_data_managers)

    btc1min = raw_data_managers['binanceBTCUSDT1m']

    btc5min = raw_data_managers['binanceBTCUSDT5m']

    btc15min = raw_data_managers['binanceBTCUSDT15m']

    btc30min = raw_data_managers['binanceBTCUSDT30m']

    btc1h = raw_data_managers['binanceBTCUSDT1h']

    btc4h = raw_data_managers['binanceBTCUSDT4h']

    dumb = DumbStrategy(btc1min, btc5min, btc15min, btc30min, btc1h, btc4h)

    backtest = Simulator(dumb, 0.075)

    # backtest.plot_pnl()

    #bol_strategy = BollingerStrategy(btc1min)

    #bol_batch = BollingerBatch(btc1min)

    # backtest.save_to_disk()

