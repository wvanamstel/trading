# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 11:12:16 2015

@author: w
"""
import Queue
import threading
import time

from execution import Execution
from settings import STREAM_DOMAIN, API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID
from strategy import TestRandomStrategy
from streaming import StreamingForexPrices

def trade(events, strategy, execution):
#==============================================================================
#     Carries out infinite while loop that polls the events queue and directs
#     each event to either the strategy component or execution handler. Loop
#     pauses for the heartbeat.
#==============================================================================
    while True:
        try:
            event = events.get(False)
        except Queue.Empty:
            pass
        else:
            if event is not None:
                if event.type == 'TICK':
                    strategy.calc_signals(event)
                elif event.type == 'ORDER':
                    print 'Executing order'
                    execution.execute_order(event)
        time.sleep(heartbeat)
        
        
if __name__ == '__main__':
    heartbeat = 0.5
    events = Queue.Queue()
    
    # define instrument and size
    instrument = 'EUR_USD'
    units = 10000
    
    # create oanda price streaming class providing authentication
    prices = StreamingForexPrices(STREAM_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID,
                                  instrument, events)
    
    # create execution handler
    execution = Execution(API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID)
    
    # create strategy/signal generator
    strategy = TestRandomStrategy(instrument, units, events)
    
    # create threads
    trade_thread = threading.Thread(target=trade, args=(events, strategy, execution))
    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])
    
    # start threads
    trade_thread.start()
    price_thread.start()