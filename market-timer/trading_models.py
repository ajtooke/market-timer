from stock import Stock

class TradingModel:
	"""Superclass of stock trading models."""
	
	# All TradingModels share a dictionary of stock objects
	stock_objs = dict()

	# Start and end dates are also shared between models
	start_date = None;
	end_date = None;

	def __init__(self, start_date=None, end_date=None):
		if start_date and end_date:
			self.start_date = start_date
			self.end_date = end_date

	def get_stock_obj(self, symbol):
		pass

	def set_stock_obj(self, symbol):
		if not (symbol in self.stock_objs):
			self.stock_objs[symbol] = Stock(symbol, self.start_date, self.end_date)

class HoldSPY(TradingModel):
	"""Stock trading model that holds SPY."""

	def __init__(self, start_date, end_date):
		super().__init__(start_date, end_date)
		self.set_stock_obj('SPY')

		num_trading_days = len(self.stock_objs['SPY'].date)
		self.symbol_seq = ['SPY' for x in range(num_trading_days)]
		
class HoldIEF(TradingModel):
	"""Stock trading model that holds SPY."""

	def __init__(self, start_date, end_date):
		super().__init__(start_date, end_date)
		self.set_stock_obj('IEF')

		num_trading_days = len(self.stock_objs['IEF'].date)
		self.symbol_seq = ['IEF' for x in range(num_trading_days)]
		