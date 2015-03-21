# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 17:55:48 2015

@author: w
"""
from decimal import Decimal, getcontext, ROUND_HALF_DOWN

class Position(object):
    def __init__(self, side, market, units, exposure, avg_price, cur_price):
        self.side = side  # long or short
        self.market = market  # currency pair
        self.units = units  # amount of units
        self.exposure = Decimal(str(exposure))  # money exposure in base currency
        self.avg_price = Decimal(str(avg_price))  # average price of position
        self.cur_price = Decimal(str(cur_price))  # current price of currency pair
        self.profit_base = self.calc_profit_base()  # current pnl in base cur
        self.profit_perc = self.calc_profit_perc()  # current % pnl of position

    def calc_pips(self):
        # calc amount of pips generated by total position
        mult = 1
        if self.side == 'SHORT':
            mult = -1
        return (mult * (self.cur_price - self.avg_price)).quantize(Decimal("0.00001"), ROUND_HALF_DOWN)
    
    def calc_profit_base(self):
        # calc nominal pnl of total position
        pips = self.calc_pips()
        return (pips * self.exposure / self.cur_price).quantize(Decimal("0.00001"), ROUND_HALF_DOWN)
    
    def calc_profit_perc(self):
        # calc relative pnl of total position
        return (self.profit_base / self.exposure * Decimal('100.00')).quantize(Decimal("0.00001"), ROUND_HALF_DOWN)
    
    def update_position_price(self, cur_price):
        # update pnl metrics to current instrument price
        self.cur_price = cur_price
        self.profit_base = self.calc_profit_base()
        self.profit_perc = self.calc_profit_perc()
        