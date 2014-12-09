# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 16:21:25 2014

@author: w
"""

import Quandl as q
import pandas as pd
import numpy as np

from backtest import Portfolio, Strategy

class SimpleStrategy(Strategy):
    def __init__(self, symbol, bars):
        self.symbol = symbol
        self.bars = bars
        
    def generate_signals(self):
        # signal df with index only
        signal = pd.DataFrame(index=self.bars.index)
        #simple moving avg strategy
        mavg50 = pd.stats.moments.rolling_mean(self.bars['Close'], 50)
        mavg200 = pd.stats.moments.rolling_mean(self.bars['Close'], 200)
        
        signal['sig'] = mavg50 < mavg200
        signal['sig'] = signal['sig'].apply(lambda x: -1 if x==False else 1)
        signal['sig'][0:250] = 0.0        
        
        return signal
        
class MavgPortfolio(Portfolio):
    def __init__(self, symbol, bars, signal, init_capital=10000):
        self.symbol = symbol
        self.bars = bars
        self.signal = signal
        self.init_capital = float(init_capital)
        self.pos = self.generate_positions()
    
    def generate_positions(self):
        pos = pd.DataFrame(index=self.signal.index).fillna(0.0)
        pos[self.symbol] = 100*self.signal['sig']
        
        return pos
    
    def backtest_portfolio(self):
        portfolio = self.pos*self.bars['Open']
        pos_diff = self.pos.diff()
        
        portfolio['holdings'] = (self.pos*self.bars['Open']).sum(axis=1)
        portfolio['cash'] = self.init_capital - (pos_diff*self.bars['Open']).sum(axis=1).cumsum()
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
        
        return portfolio

if __name__=='__main__':
    symbol = 'AA'
    bars = q.get('GOOG/NYSE_%s' % symbol, collapse='daily')
    
    strat = SimpleStrategy(symbol, bars)
    signal = strat.generate_signals()
    
    port = MavgPortfolio(symbol, bars, signal, init_capital=10000)
    ret = port.backtest_portfolio()
    
    print ret.tail(10)
    
    