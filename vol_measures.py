# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 16:22:57 2015

@author: w
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class VolatilityMeasures(object):
    def __init__(self, data, window=60, total_days=252):
        self.data = data
        self.window = window
        self.total_days = total_days
        
    def close_close(self):
        log_return = (self.data['Close']/self.data['Close'].shift(1)).apply(np.log)
        vol = pd.rolling_std(log_return, self.window) * np.sqrt(self.total_days)
        vol.index = self.data['Date']
        
        return vol

    def rogers_satchell(self):
        #rogers satchell yoon estimator
        log_hc = (self.data['High']/self.data['Close']).apply(np.log)
        log_ho = (self.data['High']/self.data['Open']).apply(np.log)
        log_lo = (self.data['Low']/self.data['Open']).apply(np.log)
        log_lc = (self.data['Low']/self.data['Close']).apply(np.log)
        
        rsy = log_hc * log_ho + log_lc * log_lo
        
        out = self.annualise(rsy)   
        out.index = self.data['Date']
        
        return out
    
    def parkinson(self):
        log_hl = (self.data['High']/self.data['Low']).apply(np.log)

        park = (1/(4*np.log(2))) * log_hl**2
        
        out = self.annualise(park)
        out.index = self.data['Date']
        
        return out
        
    def garman_klass(self):
        log_hl = (self.data['High'] / self.data['Low']).apply(np.log)
        log_co = (self.data['Close'] / self.data['Open']).apply(np.log)
        log_oc = (self.data['Open'] / self.data['Close']).apply(np.log)
        
        
    def annualise(self, daily_vols):
        return (pd.rolling_mean(daily_vols, self.window) * self.total_days)\
               .apply(lambda x: x if not x else np.sqrt(x))
        
        
if __name__=='__main__':
    data = pd.read_csv('/home/w/code/python/trading/data/50etf.csv')
    vol = VolatilityMeasures(data)
    clcl = vol.close_close()
    rs = vol.rogers_satchell()
    p = vol.parkinson()
    #clcl2 = vol.close_close(data, 90)
    #rs = vol.rogers_satchell(data, 30)
    #rs.plot()
    #clcl.plot()
    #data['Close'].plot()
    
    fig, ax1 = plt.subplots()
    ax1.plot(p, color='red', lw=2)
    ax1.set_ylabel('30d Close/Close vol', color='red')

    ax2 = ax1.twinx()
    #ax2.plot(data['Close'], color='blue', lw=2)
    #ax2.set_ylabel('Price', color='blue')
    ax2.plot(rs)
    plt.title('2 lines')
    plt.show()
