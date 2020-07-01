import backtrader as bt

# this is a strategy to buy slight dips

# Create a Stratey
class TestStrategyDip(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None

    # receives order object and check on status
    def notify_order(self,order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        #if the order is completed we record the execution price
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED{}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED{}'.format(order.executed.price))
        
            #tracks the current bar
            self.bar_executed = len(self)
        #after it's recorded we reset
        self.order = None


    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        #if we are not in the position, we are gonna buy
        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        
        #if we are in the position we need to look at when we sell
        else:
            if len(self) >= (self.bar_executed):
                self.log('SELL CREATE {}'.format(self.dataclose[0]))
                self.order = self.sell()