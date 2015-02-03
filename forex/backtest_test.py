# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 17:59:32 2015

@author: w
"""
import pandas as pd
import numpy as np

from backtest import Portfolio, Strategy

class TestStrat(Strategy):
    def __init__(self, instrument, quotes):
        self.instrument = instrument
        self.orders = orders
        
    def generate_signals(self):
        # generate signals based on a simple moving average strategy
    