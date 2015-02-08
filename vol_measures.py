# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 16:22:57 2015

@author: w
"""
import pandas as pd
import numpy as np


class VolatilityMeasures(object):
    def __init__(self, data, window=30, total_days=252):
        self.data = data
        self.window = window
        self.total_days = total_days

    def close_close(self):
        log_return = (self.data['Close']/self.data['Close'].shift(1)).apply(np.log)
        vol = pd.rolling_std(log_return, self.window) * np.sqrt(self.total_days)
        vol.index = self.data['Date']

        return vol

    def rs(self):
        # rogers satchell yoon estimator
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

    def gk(self):
        # garman klass, no opening jumps
        log_hl = (self.data['High'] / self.data['Low']).apply(np.log)
        log_co = (self.data['Close'] / self.data['Open']).apply(np.log)

        gk = 1./2 * log_hl**2 - (2 * np.log(2) - 1) * log_co**2
        out = self.annualise(gk)
        out.index = self.data['Date']

        return out

    def gkyz(self):
        # garman klass yang zhang
        log_oc = (self.data['Open']/self.data['Close'].shift(1)).apply(np.log)
        log_hl = (self.data['High']/self.data['Low']).apply(np.log)
        log_co = (self.data['Close']/self.data['Open']).apply(np.log)

        log_hl[self.window - 1] = np.nan
        log_co[self.window - 1] = np.nan

        gkyz = log_oc**2 + 1./2 * log_hl**2 - (2*np.log(2) - 1)*log_co**2

        out = self.annualise(gkyz)
        out.index = self.data['Date']

        return out

    def yz(self):
        # yang zhang
        log_oc = (self.data['Open']/self.data['Close'].shift(1)).apply(np.log)

        log_co = (self.data['Close']/self.data['Open']).apply(np.log)

        s2rs = self.rs().values**2
        s2o = pd.rolling_var(log_oc, self.window) * self.total_days
        s2c = pd.rolling_var(log_co, self.window) * self.total_days

        # adjust other vol measures for the lag in open/close vol
        s2rs[self.window-1] = np.nan
        s2c[self.window-1] = np.nan

        k = 0.34/(1. + (self.window + 1.)/(self.window - 1.))

        out = (s2o + k * s2c + (1-k)*s2rs).apply(np.sqrt)
        out.index = self.data['Date']

        return out

    def annualise(self, daily_vols):
        return (pd.rolling_mean(daily_vols, self.window) * self.total_days)\
                .apply(lambda x: x if not x else np.sqrt(x))
