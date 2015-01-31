# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 16:56:32 2015

@author: w
"""

import requests
import pandas as pd

from settings import API_DOMAIN, ACCESS_TOKEN


class HistoricalPrices(object):
    def __init__(self, instrument, window, access_token, api_domain):
        self.instrument = instrument
        self.window = window
        self.access_token = access_token
        self.api_domain = API_DOMAIN

    def fetch_prices(self):
        # open a session with oanda and fetch prices
        try:
            s = requests.Session()
            headers = {'Authorization' : 'Bearer ' + self.access_token}
            params  = {'instrument' : self.instrument}
            url = 'https://' + self.api_domain + '/v1/candles'
            req = requests.Request('GET', url, headers=headers, params=params)
            prep = req.prepare()
            resp = s.send(prep, verify=False)
            s.close()
        except Exception as e:
            print 'Error fetching historical prices' + str(e)
            return -1

        # extract price info from server response and return as dataframe
        content = resp.json()
        candles = content['candles']
        df = pd.DataFrame(candles)
        df = df.drop('complete', axis=1)
        df['time'] = pd.to_datetime(df['time'])
        indexed_df = df.set_index('time')

        return indexed_df

if __name__ == '__main__':
    hist = HistoricalPrices('EUR_USD', 30, ACCESS_TOKEN, API_DOMAIN)
    prices = hist.fetch_prices()
