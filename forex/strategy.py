# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 20:56:04 2015

@author: w
"""

import random
from events import OrderEvent

class TestRandomStrategy(object):
    def __init__(self, instrument, units, events):
        self.instrument = instrument
        self.units = units
        self.events = events
        self.ticks = 0
        
    def calc_signals(self, event):
        if event.type = 'TICK':
            self.ticks += 1
            if self.ticks % 5 == 0:
                side = random.choice(['buy', 'sell'])
                order = OrderEvent(self.instrument, self.units, 'market', side)
                self.events.put(order)