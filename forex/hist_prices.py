# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 16:56:32 2015

@author: w
"""

import requests
import pandas as pd

from settings import API_DOMAIN, ACCESS_TOKEN


class HistoricalPrices(object):
    def __init__(self, instrument, num_quotes, 
                 granularity, access_token, api_domain):
        self.instrument = instrument
        self.num_quotes = num_quotes
        self.granularity = granularity
        self.access_token = access_token
        self.api_domain = API_DOMAIN

    def fetch_prices(self):
        # open a session with oanda and fetch prices
        try:
            headers = {'Authorization' : 'Bearer ' + self.access_token}
            params  = {'instrument' : self.instrument, 
                       'granularity' : self.granularity,
                       'count' : self.num_quotes}
            url = 'https://' + self.api_domain + '/v1/candles'
            resp = requests.get(url, headers=headers, params=params)
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
        
        # rearrange columns
        cols = ['openBid', 'openAsk', 'highBid', 'highAsk', 'lowBid', 'lowAsk',
                'closeBid', 'closeAsk', 'volume']
        indexed_df = indexed_df[cols]
        return indexed_df

if __name__ == '__main__':
    hist = HistoricalPrices('EUR_USD', 30, 'M1', ACCESS_TOKEN, API_DOMAIN)
    prices = hist.fetch_prices()
