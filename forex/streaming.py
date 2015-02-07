# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 10:42:59 2015

@author: w
"""

import requests
import json

from events import TickEvent

class StreamingForexPrices(object):
    def __init__(self, domain, access_token, account_id, 
                 instruments, events_queue):
        self.domain = domain
        self.access_token = access_token
        self.account_id = account_id
        self.instruments = instruments
        self.events_queue = events_queue
        self.cur_bid = None
        self.cur_ask = None
        
    def connect_to_stream(self):
        try:
            s = requests.Session()
            url = "https://" + self.domain + "/v1/prices"
            headers = {'Authorization' : 'Bearer ' + self.access_token}
            params = {'instruments' : self.instruments, 
                      'accountId' : self.account_id}
            req = requests.Request('GET', url, headers=headers, params=params)
            pre = req.prepare()
            resp = s.send(pre, stream=True, verify=False)
            return resp
        except Exception as e:
            s.close()
            print "Caught exception when connecting to stream\n" + str(e)

            
    def stream_to_queue(self):
        response = self.connect_to_stream()
        if response.status_code != 200:
            print 'Error connecting to quote stream'
            print response.status_code
            return
        for line in response.iter_lines(1):
            if line:
                try:
                    msg = json.loads(line)
                except Exception as e:
                    print 'Error converting into json:\n' + str(e)
                    return
                if msg.has_key('instrument') or msg.has_key('tick'):
                    print msg
                    instrument = msg['tick']['instrument']
                    time = msg['tick']['time']
                    bid = msg['tick']['bid']
                    ask = msg['tick']['ask']
                    self.cur_bid = bid
                    self.cur_ask = ask
                    tev = TickEvent(instrument, time, bid, ask)
                    self.events_queue.put(tev)