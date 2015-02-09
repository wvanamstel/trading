# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pandas.io.data as web
import datetime
import urllib2
import time
import re


class GetData(object):
    ''' Fetch minute data from Google
        IN: all strings; symbol, interval in secs, time period, open/close/etc
        OUT: data frame with historical minute prices
    '''
    def __init__(self, interval='60', period='5d', dat='d,o,h,l,c,v'):
        self.interval = interval  # default is 60 seconds
        self.period = period  # number of days history, default is 5
        self.dat = dat  # 'date', 'open', 'high', etc

    def get_minute_data(self, symbol):
        print 'Fetching data'

        url = 'http://www.google.com/finance/getprices?' + \
                   'i=' + self.interval + \
                   '&p=' + self.period + \
                   '&f=' + self.dat + \
                   '&q=' + symbol.upper()
        request = urllib2.Request(url)
        raw_data = urllib2.urlopen(request).readlines()
        raw_data = raw_data[7:]  # strip headers from received data

        time_stamps = []
        quotes = []
        for line in raw_data:
            line = line.strip('\n')
            line = line.split(',')
            # set correct time stamp, the base stamp is in 'a1415277322' epoch
            # format, for consecutive quotes  in the same day, there is an
            # offset number
            if list(line[0])[0] == 'a':
                date_base = float(line[0].strip('a'))
                date_offset = 0
            else:
                date_offset = float(line[0]) * float(self.interval)

            time_stamps.append(time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime(date_base +
                                             date_offset)))

            prices = []
            prices.extend([float(x) for x in line[1:]])
            quotes.append(prices)

        quotes = np.array(quotes)

        cols_raw = ['Close', 'High', 'Low', 'Open', 'Volume']
        quotes_out = pd.DataFrame(quotes, index = time_stamps, columns=cols_raw)
        quotes_out.index = pd.to_datetime(quotes_out.index, unit='m')
        # rearrange columns to normal order
        cols_target = ['Open', 'High', 'Low', 'Close', 'Volume']
        quotes_out = quotes_out[cols_target]

        return quotes_out

    def get_daily_data(self, symbol):
        end = datetime.date.today()
        t = datetime.timedelta(days=360)
        start = end - t
        
        quotes = web.DataReader(symbol.upper(), 'google', start, end)
        
        return quotes
        
    def get_china_data(self, symbol, adjusted=True):
        end = datetime.date.today()
        t = datetime.timedelta(days=360)
        start = end - t
        symbol = symbol + '.SS'        
        
        quotes = web.DataReader(symbol, 'yahoo', start, end)
        # adjust for divs/splits if required, default is true
        if adjusted:
            adj = quotes['Adj Close']/quotes['Close']
            out = quotes[['Open', 'High', 'Low', 'Close']] * adj
            out['Volume'] = quotes['Volume']
            return out
        else:
            return quotes

    def get_multiple_quotes(self, symbol_list):
        '''
        IN: list, symbols
        OUT: data frame of closing prices of symbols
        '''
        quotes_out = pd.DataFrame()
        for sym in symbol_list:
            temp = self.get_data(sym)
            quotes_out[sym.upper()] = temp['Close']

        return quotes_out

    def get_rt_quote(self, symbol):
        '''
        Retrieve current quote from google finance
        IN: string; quote symbol
        OUT: price and timestamp
        '''
        url = 'http://www.google.com/finance?&q=' + symbol
        request = urllib2.Request(url)
        result = urllib2.urlopen(request).read()
        quote = re.search('id="ref_(.*?)">(.*?)<', result)

        if quote:
            tmp = quote.group(2)
            price = tmp.replace(',', '')
        else:
            price = 'Error accessing google finance'

        return price, time.ctime()


if __name__ == '__main__':
    a = GetData(period='1d')
    lst = 'JNPR'
    quotes = a.get_minute_data(lst)
    #test = a.get_minute_data('EURUSD')
    
#==============================================================================
#     for i in range(5):
#         for sym in ['EURUSD',2]:
#             print time.ctime()
#             print sym + ' ' + a.get_rt_quote(sym)[0]
#             
#         print '========================'
#         time.sleep(60)
#==============================================================================

