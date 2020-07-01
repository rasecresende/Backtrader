from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

import backtrader as bt
import datetime
from SMAcross import SmaCross

if __name__ == '__main__':
    #instantiates cerebro engine (creates broker instance in the background)
    cerebro = bt.Cerebro()

    #changes the initial cash value
    cerebro.broker.set_cash(10000)

    #creates data feed
    datalist = [('PETR4.SA.csv', 'PTR4'), ('ITUB4.SA.csv', 'ITUB4'), ('ABEV3.SA.csv', 'ABEV3')]

    for i in range(len(datalist)):
        data = bt.feeds.YahooFinanceCSVData(dataname=datalist[i][0])
        cerebro.adddata(data, name = datalist[i][1])

    #add a strategy
    cerebro.addstrategy(SmaCross)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())


    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()