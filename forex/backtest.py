'''
derived from equity backtester
'''

from abc import ABCMeta, abstractmethod

class Strategy(object):
	___metaclass__ = ABCMeta

	@abstractmethod
	def generate_signals(self):
		'''An implementation is required to return the DataFrame of symbols 
		containing the signals to go long, short or hold (1, -1 or 0)'''
		raise NotImplementedError("Should implement generate_signals()")

class Portfolio(object):
	___metaclass__ = ABCMeta

	@abstractmethod
	def generate_positions(self):
		''' Generate positions based on signals constructed in the strategy
         class.'''
		raise NotImplementedError("Should implement generate_positions()")

	@abstractmethod
	def backtest_portfolio(self):
		'''Provides the logic to generate the trading orders
		and subsequent equity curve'''
		raise NotImplementedError("Should implement backtest_portfolio()")
