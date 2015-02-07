# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 20:56:04 2015

@author: w
"""

from events import SignalEvent

class TestStrategy(object):
    def __init__(self, instrument, units, events):
        self.instrument = instrument
        self.units = units
        self.events = events
        self.ticks = 0
        self.invested = False
        
    def calc_signals(self, event):
        #stupid random buy/sell on every 5th tick
        if event.type == 'TICK':
            self.ticks += 1
            if self.ticks % 5 == 0:
                if self.invested == False:
                    signal = SignalEvent(instrument, 'market', 'buy')
                    self.events.put(signal)
                    self.invested = True
                else:
                    signal = SignalEvent(instrument, 'market', 'sell')
                    self.events.put(signal)
                    self.invested = False
                