import datetime
from yahoo_finance import Share
from csv import DictReader
from urllib.request import urlopen
from io import StringIO
import numpy as np
import pdb

class Stock:
    """Stock class that holds symbol, price history with corresponding dates, 
    dividends, and other useful info."""

    def __init__(self, symbol, start_date=None, end_date=None):

        self.symbol = symbol
        self.yf_share = Share(symbol)
        self.date = []
        self.open_value = None
        self.close_value = None
        self.low = None
        self.high = None
        self.volume = None
        self.adj_close = None
        self.dividend = None

        if start_date and end_date:
            self.populate_data(start_date, end_date)

    def populate_data(self, start_date, end_date, mask='%Y-%m-%d'):
        """
        Populates historical stock data between start_date and end_date, 
        inclusive.

        start_date: string 'yyyy-mm-dd'
        end_date: string 'yyy-mm-dd'
        """

        start_date_num = [int(x) for x in start_date.split('-')]
        end_date_num = [int(x) for x in end_date.split('-')]

        self.start_date = datetime.date(start_date_num[0], start_date_num[1], start_date_num[2])
        self.end_date = datetime.date(end_date_num[0], end_date_num[1], end_date_num[2])

        if self.start_date > self.end_date:
            raise ValueError('Start date "%s" is greater than "%s"' % 
                (self.start_date, self.end_date))

        hist = self.yf_share.get_historical(start_date, end_date)
        hist_div = get_dividend_history(self.symbol, self.start_date, self.end_date)

        # import all data to numpy arrays, and dates to a list.
        date_temp = []
        open_value_temp = []
        close_value_temp = []
        low_temp = []
        high_temp = []
        volume_temp = []
        adj_close_temp = []
        dividend_temp = []
        for l in hist:
            date_num = [int(x) for x in l['Date'].split('-')]
            date_temp.append(datetime.date(date_num[0], date_num[1], date_num[2]))
            open_value_temp.append(float(l['Open']))
            close_value_temp.append(float(l['Close']))
            low_temp.append(float(l['Low']))
            high_temp.append(float(l['High']))
            volume_temp.append(float(l['Volume']))
            adj_close_temp.append(float(l['Adj_Close']))

        # Ensure dates are sorted and get indices.
        ind = [i[0] for i in sorted(enumerate(date_temp), key=lambda x:x[1])]

        self.date = [date_temp[i] for i in ind]

        # Convert all lists to numpy arrays.
        self.open_value = np.array([open_value_temp[i] for i in ind])
        self.close_value = np.array([close_value_temp[i] for i in ind])
        self.low = np.array([low_temp[i] for i in ind])
        self.high = np.array([high_temp[i] for i in ind])
        self.volume = np.array([volume_temp[i] for i in ind])
        self.adj_close = np.array([adj_close_temp[i] for i in ind])
        self.dividend = np.zeros(self.open_value.size)

        # Correctly set dividends
        for l in hist_div:
            date_num = [int(x) for x in l['Date'].split('-')]
            date_temp = datetime.date(date_num[0], date_num[1], date_num[2])
            if date_temp in self.date:
                self.dividend[self.date.index(date_temp)] = \
                    float(l['Dividends'])

def get_dividend_history(symbol, start_date, end_date):
    """take in start_date and end_date datetime.date objects and create the 
    correct URL to grab csv data from. Also requires stock symbol"""

    url_base = 'http://ichart.finance.yahoo.com/table.csv'

    url = (url_base + '?' + 
        's=' + symbol + '&' +
        'a=' + str(start_date.month - 1) + '&' +
        'b=' + str(start_date.day) + '&' +
        'c=' + str(start_date.year) + '&' +
        'd=' + str(end_date.month - 1) + '&' +
        'e=' + str(end_date.day) + '&' +
        'f=' + str(end_date.year) + '&' +
        'g=v')

    response = urlopen(url).read().decode('utf-8')
    cr = DictReader(StringIO(response))

    return cr