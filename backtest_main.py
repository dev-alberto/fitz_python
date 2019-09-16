from db_connect import Connect
from rpc.rpc_bridge import RpcBridge
from rpc.db_bridge import DbBridge
from instance import Instance


from strategy.bollinger.boll2 import BollingerImpl2
from strategy.bollinger.bollinger_strategy import BollingerStrategy
from strategy.bollinger.bollinger_batch import BollingerBatch

from feature.LogReturns import LogReturns
from strategy.returns.returns import Returns0

from strategy.backtest.simulator import Simulator

from data_retriever import *


from feature.LogReturns import LogReturns


if __name__ == '__main__':
    
    # conn = Connect('fitz.db')
    conn = Connect('binance_0.1.db')

    cur = conn.cursor()

    symbol = 'BTCUSDT'
    period = '1m'
    exchange = 'binance'

    # data = Get_candlesticks_between_dates(cur, "2019-7-12-17-0-0", "2019-7-16-18-0-0", period,symbol,exchange)
    # data = Get_all_candlesticks_with_period(cur, period,symbol,exchange)

    data = Get_gecko_data(cur, symbol)
    
    js = {'symbols': [{'symbol': symbol, 'periods': ['1m'], 'exchange': 'binance', 'state': 'watch', 'history': len(data),'strategies': []}]}

    ii = Instance()
    
    db_bridge = DbBridge(ii)
    db_bridge.instantiate(js)

    db_bridge.backfill(exchange, symbol, period, data)

    raw_data_managers = ii.get_raw_data_managers()

    btc1min = raw_data_managers['binanceBTCUSDT1m']
    

    bol_strategy = BollingerStrategy(btc1min)

    #bol_batch = BollingerBatch(btc1min)

    backtest = Simulator(bol_strategy, 0.075)

    backtest.plot_pnl()

    # backtest.save_to_disk()

