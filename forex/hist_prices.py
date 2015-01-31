# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 16:56:32 2015

@author: w
"""

import requests
import httplib
import json

from settings import STREAM_DOMAIN, API_DOMAIN, ACCESS_TOKEN

class HistoricalPrices(object):
    def __init__(self, instrument, window, access_token):
        self.instrument = instrument
        self.window = window
        self.access_token = access_token

        
    def fetch_prices(self):
        s = requests.Session()
        headers = {'Authorization' : 'Bearer ' + self.access_token}
        params  = {'instrument' : self.instrument}
        url = 'https://api-fxpractice.oanda.com/v1/candles'
        req = requests.Request('GET', url, headers=headers, params=params)
        prep = req.prepare()
        resp = s.send(prep, verify=False)
        return resp

if __name__=='__main__':
    hist = HistoricalPrices('EUR_USD', 30, ACCESS_TOKEN)
    prices = hist.fetch_prices()
    