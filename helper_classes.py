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
    def __init__(self, symbol, interval='60', period='5d', dat='d,o,h,l,c,v'):
        self.symbol = symbol.upper()
        self.interval = float(interval)
        self.url = 'http://www.google.com/finance/getprices?' + \
                   'i=' + interval + \
                   '&p=' + period + \
                   '&f=' + dat + \
                   '&q=' + symbol.upper()

    def get_data(self):
        print 'Fetching data'
        request = urllib2.Request(self.url)
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
                date_offset = float(line[0]) * self.interval

            time_stamps.append(time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime(date_base +
                                             date_offset)))

            prices = []
            prices.extend([float(x) for x in line[1:]])
            quotes.append(prices)

        quotes = np.array(quotes)

        cols_raw = ['Close', 'High', 'Low', 'Open', 'Volume']
        quotes_out = pd.DataFrame(quotes, index = time_stamps, columns=cols_raw)
        # rearrange columns to normal order
        cols_target = ['Open', 'High', 'Low', 'Close', 'Volume']
        quotes_out = quotes_out[cols_target]

        return quotes_out

if __name__ == '__main__':
    a = MinuteData('msft')
    test = a.get_data()
