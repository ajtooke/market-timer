from stock import Stock
import numpy as np
import math

class TradingModel:
	"""Superclass of stock trading models."""
	
	# All TradingModels share a dictionary of stock objects
	stock_objs = dict()

	# Start and end dates are also shared between models
	start_date = None;
	end_date = None;

	# Store a common copy of dates
	date = None

	def __init__(self, start_date=None, end_date=None):
		"""start_date: string 'yyyy-mm-dd'
        end_date: string 'yyy-mm-dd' """

		if start_date and end_date:
			self.start_date = start_date
			self.end_date = end_date

		# initialize all arrays to simulate return
		# these contain value of investments and number of shares
		self.invested_value = None
		self.invested_shares = None

		# dividend_value = dividend/share * invested_shares
		self.dividend_value = None

		# after selling, no dividend included
		self.cash_after_sell = None

		# before executing buy, after receiving dividend for current day
		self.cash_before_buy_after_div = None

		# after executing buy
		self.cash_after_buy_and_div = None

		# end of day total value (close price and cash)
		self.end_of_day_value = None

	def get_stock_obj(self, symbol):
		pass

	def set_stock_obj(self, symbol):
		if not (symbol in self.stock_objs):
			self.stock_objs[symbol] = Stock(symbol, self.start_date, self.end_date)
		if not self.date:
			self.date = self.stock_objs[symbol].date

	def add_model_return(self):
		"""function add_model_return takes in a TradingModel object and adds its
		total return over time, given price history, dividend history and symbols."""

		# start with $10k
		START_CASH = float(10000)

		# preallocate numpy arrays. index 1 corresponds to day 0.
		numel = len(self.symbol_seq)
		self.invested_value = np.zeros(numel+1)
		self.invested_shares = np.zeros(numel+1)
		self.dividend_value = np.zeros(numel+1)
		self.cash_after_sell = np.zeros(numel+1)
		self.cash_before_buy_after_div = np.zeros(numel+1)
		self.cash_after_buy_and_div = np.zeros(numel+1)

		self.cash_after_buy_and_div[0] = START_CASH

		# loop through days seems easiest for now ...
		for i in range(len(self.symbol_seq)):

			# get today's dividend
			self.dividend_value[i+1] = (self.invested_shares[i] * 
				self.stock_objs[self.symbol_seq[i]].dividend[i])

			self.cash_after_sell[i+1] = self.cash_after_buy_and_div[i]

			# get and add sell value if sell is signaled
			if i > 0:
				sell_signal = not (self.symbol_seq[i-1] == self.symbol_seq[i])
			else:
				sell_signal = False

			if sell_signal:
				sell_value = (self.invested_shares[i] * 
					self.stock_objs[self.symbol_seq[i-1]].open_value[i])
			else:
				sell_value = 0

			self.cash_after_sell[i+1] += sell_value
			
			self.cash_before_buy_after_div[i+1] = (self.cash_after_sell[i+1] + 
				self.dividend_value[i+1])

			current_value = self.stock_objs[self.symbol_seq[i]].open_value[i]
			shares_to_buy = math.floor(
				self.cash_before_buy_after_div[i+1] / current_value)

			self.invested_shares[i+1] = self.invested_shares[i] + shares_to_buy
			self.invested_value[i+1] = self.invested_shares[i+1] * current_value

			# adjust remaining cash
			self.cash_after_buy_and_div[i+1] = (self.cash_before_buy_after_div[i+1] - 
				(shares_to_buy * current_value))

		self.end_of_day_value = self.cash_after_buy_and_div + self.invested_value

	def plot_model_return(self):

		if not (self.invested_value):
			self.add_model_return()

		# Plot various value metrics.

class MACModel(TradingModel):
	"""Moving-average crossover trading model implementation."""

	def __init__(self, symbols, start_date, end_date, 
		ema_days_low=34, ema_days_high=200, ma_days_low=40, ma_days_high=200):
		"""symbols is a list of two symbols to apply model to -- stock fund first, then bond.
		Start_date and end_date are same as always"""
		super().__init__(start_date, end_date)
		for sym in symbols:
			self.set_stock_obj(sym)

		# calculate exponential moving average alpha parameters
		# use 99.9% of weight (0.001 not included)
		self.alpha_low = 1 - math.exp(math.log(0.001) / ema_days_lows)
		self.alpha_high = 1 - math.exp(math.log(0.001) / ema_days_high)

		# calculate EMA for stock series




class HoldSymbol(TradingModel):
	"""Stock trading model that holds a given symbol."""

	def __init__(self, symbol, start_date, end_date):
		super().__init__(start_date, end_date)
		self.set_stock_obj(symbol)

		num_trading_days = len(self.stock_objs[symbol].date)
		self.symbol_seq = [symbol for x in range(num_trading_days)]


def hold_spy(start_date, end_date):
	"""Stock trading model that holds SPY."""

	return HoldSymbol('SPY', start_date, end_date)
		
def hold_ief(start_date, end_date):
	"""Stock trading model that holds SPY."""
		
	return HoldSymbol('IEF', start_date, end_date)