from ib_insync import *
import pandas as pd

ib = IB()
ib.connect(host='127.0.0.1', port=4002)

contract = Stock('AMD', exchange='SMART', currency='USD')
ib.qualifyContracts(contract)

market_data = ib.reqMktData(contract, '', False, False)

def onPendingTickers(tickers):
    print('data recieved')
    print(ticker)
# bars = ib.reqHistoricalData(contract, '', '2 D', '15 mins', 'MIDPOINT', useRTH=True)

ib.pendingTickersEvent += onPendingTickers
ib.run()

# df = pd.DataFrame(bars)
# print(df)

