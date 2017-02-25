from datetime import datetime
from yahoo_finance import Share
import pdb

class Stock:
    """Stock class that holds symbol, price history with corresponding dates, 
    dividends, and other useful info."""

    data = dict()

    def __init__(self, symbol):
        self.symbol = symbol
        self.yf_share = Share(symbol)

    def populate_data(self, start_date, end_date, mask='%Y-%m-%d'):
        """
        Populates historical stock data between start_date and end_date, 
        inclusive.

        start_date: string 'yyyy-mm-dd'
        end_date: string 'yyy-mm-dd'
        """

        self.start_date = datetime.strptime(start_date, mask)
        self.end_date = datetime.strptime(end_date, mask)

        if self.start_date > self.end_date:
            raise ValueError('Start date "%s" is greater than "%s"' % 
                (self.start_date, self.end_date))

        hist = self.yf_share.get_historical(start_date, end_date)
        hist_div = self.yf_share.get_historical_dividends(start_date, end_date)

        # new combined dict with first key the date, and inside a dict with 
        # all info including dividend
        keys_hist = ['open_value', 'close_value', 'low', 'high', 
            'volume', 'adj_close', 'dividend']
        for l in hist:
            self.data[datetime.strptime(l['Date'], mask)] = dict(zip(keys_hist, 
                [float(l['Open']), float(l['Close']), 
                float(l['Low']), float(l['High']), 
                float(l['Volume']), float(l['Adj_Close']), float(0)]))

        pdb.set_trace()

        for l in hist_div:
            if datetime.strptime(l['Date'], mask) in self.data:
                self.data[datetime.strptime(l['Date'], mask)]['dividend'] = \
                    float(l['Dividends'])