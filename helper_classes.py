# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import urllib2
import time


class MinuteData(object):
    ''' Fetch minute data from Google
        IN: all strings; symbol, interval in secs, time period, open/close/etc
        OUT: data frame with historical minute prices
    '''
    def __init__(self, symbol, interval='60', period='1d', dat='d,o,h,l,c,v'):
        self.symbol = symbol
        self.url = 'http://www.google.com/finance/getprices?' + \
                   'i=' + interval + \
                   '&p=' + period + \
                   '&f=' + dat + \
                   '&q=' + symbol

    def get_data(self):
        print 'Fetching data'
        request = urllib2.Request(self.url)        
        raw_data = urllib2.urlopen(request).readlines()
        raw_data = raw_data[7:]
        
        quotes = np.zeros((len(raw_data), 5))
        time_stamps = []
        ind = 0
        first_entry = raw_data[0].strip('\n').split(',')
        base_stamp = first_entry[0].strip('a')
        time_stamps.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(base_stamp))))
        quotes[ind,:] = first_entry[1:]
        for line in raw_data[1:]:            
            line = line.strip('\n')
            line = line.split(',')
            time_stamps.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(base_stamp) + 60*ind)))
            ind += 1
            quotes[ind,:] = line[1:]
            
        cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        quotes_out = pd.DataFrame(quotes, index = time_stamps, columns=cols)
        
        return quotes_out
        
if __name__== '__main__':
    a = MinuteData('AA')
    test = a.get_data()