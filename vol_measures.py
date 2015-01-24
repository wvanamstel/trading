# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 16:22:57 2015

@author: w
"""
import math
import pandas as pd
import numpy as np

class VolatilityMeasures(object):
    def __init__(self):
        pass
    
    def close_close(self,data, window):
        log_return = (data['Close']/data['Close'].shift(1)).apply(np.log)
        result = pd.rolling_std(log_return, window=window) * math.sqrt(252)
        
        return result
        
if __name__=='__main__':
    vol = VolatilityMeasures()
    data = pd.read_csv('/home/w/code/python/trading/data/50etf.csv')
    clcl = vol.close_close(data, 30)
    