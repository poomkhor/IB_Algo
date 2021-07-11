import pandas as pd
from ib_insync import *

ib = IB()
ib.connect(host='127.0.0.1', port=4002)


def new_data(tickers):
    ''' process incoming data and check for trade entry '''
    for ticker in tickers:
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
    eur_usd_order = MarketOrder(direction, 100)
    trade = ib.placeOrder(eur_usd_contract, eur_usd_order)
    ib.sleep(3)
    if trade.orderStatus.status == 'Filled':
        ib.disconnect()
        quit(0)


# init dataframe
df = pd.DataFrame(columns=['date', 'last'])
df.set_index('date', inplace=True)

# Create contracts
eur_usd_contract = Forex('EURUSD', 'IDEALPRO')
usd_cad_contract = Forex('USDCAD', 'IDEALPRO')

ib.qualifyContracts(eur_usd_contract)
ib.qualifyContracts(usd_cad_contract)

# Request market data for USDCAD currency pair
ib.reqMktData(usd_cad_contract)

# Set callback function for tick data
ib.pendingTickersEvent += new_data

# Run infinitely
ib.run()