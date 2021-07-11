import pandas as pd
from ib_insync import *

ib = IB()
ib.connect(host='127.0.0.1', port=4002)


def new_data(tickers):
    ''' process incoming data and check for trade entry '''
    for ticker in tickers:
        print('data recieved')
        df.loc[ticker.time] = ticker.last
    print(df)
    five_mins_ago = df.index[-1] - pd.Timedelta(minutes=5)

    if df.index[0] < five_mins_ago:
        df = df[five_mins_ago:]

        price_min = df.last.min()
        price_max = df.last.max()

        if df.last[-1] > price_min * 1.05:
            place_order('BUY')

        elif df[-1] < price_max * 0.95:
            place_order('SELL')


def place_order(direction):
    ''' place order with IB - exit if order gets filled '''
    nflx_order = MarketOrder(direction, 100)
    trade = ib.placeOrder(nflx_contract, nflx_order)
    ib.sleep(3)
    if trade.orderStatus.status == 'Filled':
        ib.disconnect()
        quit(0)

# init dataframe
df = pd.DataFrame(columns=['date', 'last'])
df.set_index('date', inplace=True)

# Create contracts
nflx_contract = Stock('NFLX', 'SMART', 'USD')
tsla_contract = Stock('TSLA', 'SMART', 'USD')

ib.qualifyContracts(nflx_contract)
ib.qualifyContracts(tsla_contract)

# Request market data for USDCAD currency pair
ib.reqMktData(tsla_contract)

# Set callback function for tick data
ib.pendingTickersEvent += new_data

# Run infinitely
ib.run()