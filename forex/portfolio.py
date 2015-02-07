# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 18:12:40 2015

@author: w
"""

from copy import deepcopy
from events import OrderEvent
from position import Position

class Portfolio(object):
    def __init__(self, ticker, events, base='USD', leverage=20,
                 equity=100000.0, risk_per_trade=0.02):
        self.ticker = ticker  # currency pair
        self.events = events  # events queue
        self.base = base  # base currency of portfolio
        self.leverage = leverage  # gearing
        self.equity = equity  # amount of equity in account
        self.balance = deepcopy(self.equity)
        self.risk_per_trade = risk_per_trade  # maximum trade size
        self.trade_units = self.calc_risk_position_size()  #max units per pos
        self.positions = {}  # contains pos for each cur pair
        
    # crude risk mgmt position sizing
    def calc_risk_position_size(self):
        return self.equity * self.risk_per_trade
        
    def add_new_position(self, side, market, units, exposure, 
                         add_price, remove_price):
        ps = Position(side, market, units, exposure, add_price, remove_price)
        self.positions[market] = ps
        
    def add_position_units(self, market, units, exposure, 
                           add_price, remove_price):
        if market not in self.positions:
            print 'Trying to add to a non existing position'
            return False
        else:
            ps = self.positions[market]
            new_total_units = ps.units + units
            new_total_cost = ps.avg_price * ps.units + add_price * ps.units
            ps.exposure += exposure
            ps.avg_price = new_total_cost/new_total_units
            ps.units = new_total_units
            ps.update_position_price(remove_price)
            return True
            
    def remove_position_units(self, market, units, exposure, 
                              add_price, remove_price):
        if market not in self.positions:
            print 'Trying to remove from a non existing position'
            return False
        else:
            ps = self.positions[market]
            ps.units -= units
            exposure = float(units)
            ps.exposure -= exposure
            ps.update_position_price(remove_price)
            pnl = ps.calc_pips() * exposure / remove_price
            self.balance += pnl
            return True
            
    def close_position(self, market, remove_price):
        if market not in self.positions:
            print 'Trying to close a non existing position '
            return False
        else:
            ps = self.positions[market]
            ps.update_position_price(remove_price)
            pnl = ps.calc_pips() * ps.exposure / remove_price
            self.balance += pnl
            del[self.positions[market]]
            return True
            
    def execute_signal(self, signal_event):
        side = signal_event.side
        market = signal_event.instrument
        units = int(self.trade_units)
        
        # check side for correct exec price
        # ADD functionality for short trades
        add_price = self.ticker.cur_ask
        remove_price = self.ticker.cur_bid
        exposure = float(units)
        
        # If no existing position, create pos
        if market not in self.positions:
            self.add_new_position(side, market, units, exposure, 
                                  add_price, remove_price)
            order = OrderEvent(market, units, 'market', 'buy')
            self.events.put(order)
        # If pos exists, adjust
        else:
            ps = self.positions[market]
            # check if sides of the existing pos and the add are equal
            if ps.side == side:
                # add to existing pos
                self.add_position_units(market, units, exposure, 
                                        add_price, remove_price)
            else:
                # check if trade closes out position
                if units == ps.units:
                    self.close_position(market, remove_price)
                    order = OrderEvent(market, units, 'market', 'sell')
                    self.events.put(order)
                elif units < ps.units:
                    # sell from position
                    self.remove_position_units(market, units, remove_price)
                else:
                    # close existing position and add a new one consisting
                    # of the original pos adjusted with trade
                    new_units = ps.units - units
                    self.close_position(market, remove_price)
                    
                    if side == 'buy':
                        new_side = 'sell'
                    else:
                        new_side = 'buy'
                    new_exposure = float(units)
                    self.add_new_position(new_side, market, new_units,
                                          new_exposure, add_price,
                                          remove_price)
                    
        print 'Balance: %0.2f' % self.balance