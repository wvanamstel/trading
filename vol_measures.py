# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 16:22:57 2015

@author: w
"""
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class VolatilityMeasures(object):
    def __init__(self):
        pass
    
    def close_close(self,data, window=60):
        log_return = (data['Close']/data['Close'].shift(1)).apply(np.log)
        vol = pd.rolling_std(log_return, window=window) * math.sqrt(252)
        vol.index = data['Date']
        
        return vol
        
    def rogers_satchell(self, data, window=60):
        log_ho = (data['High']/data['Open']).apply(np.log)
        log_lo = (data['Low']/data['Open']).apply(np.log)
        log_co = (data['Close']/data['Open']).apply(np.log)
        
        rog_satch = log_ho * (log_ho - log_co) + log_lo * (log_lo - log_co)
        
        def f(v):
            return math.sqrt(252 * v.mean())
            
        rog_satch = pd.rolling_apply(rog_satch, window, f)
        
        return rog_satch
        
        
if __name__=='__main__':
    vol = VolatilityMeasures()
    data = pd.read_csv('/home/w/code/python/trading/data/50etf.csv')
    clcl = vol.close_close(data, 30)
    #clcl2 = vol.close_close(data, 90)
    #rs = vol.rogers_satchell(data, 30)
    #rs.plot()
    #clcl.plot()
    #data['Close'].plot()
    
    fig, ax1 = plt.subplots()
    ax1.plot(clcl, color='red', lw=2)
    ax1.set_ylabel('30d Close/Close vol', color='red')

    ax2 = ax1.twinx()
    ax2.plot(data['Close'], color='blue', lw=2)
    ax2.set_ylabel('Price', color='blue')
    plt.title('2 lines')
    plt.show()
