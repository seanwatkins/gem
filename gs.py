#!/usr/bin/env python

import time
import datetime
import httplib
import json
import random
import urllib
import logging



class GSU(object):

    def __init__ (self):

        self.api_key = "0e7249e2-7420-3a97-8987-d7a6f248d5de"    #Change This!!!
        self.component_id = "GreenEyeMonitor"
        self.base_url = "/api/feed?"

        self.headers = {"Connection" : "close", "Content-type": "application/json", 
                       "Cookie" : "api_key="+ self.api_key}




    def sendData (self, data):

        try:

            conn = httplib.HTTPConnection('www.grovestreams.com')

            url = self.base_url + urllib.urlencode (data)
        
            logging.debug ("Uploading data =  " + url)
            logging.debug ("headers = " + json.dumps(self.headers))

            conn.request ("PUT", url, "", self.headers)

            response = conn.getresponse()
            status = response.status

            if status != 200 and status != 201:
                try:
                    if (response.reason != None):
                        logging.debug('HTTP Failure Reason: ' + response.reason + ' body: ' + response.read())
                    else:
                        logging.debug('HTTP Failure Body: ' + response.read())                    
                except Exception:
                    logging.debug('HTTP Failure Status: %d' % (status) )
        
        except Exception as e:
            logging.debug('HTTP Failure: ' + str(e))
        
        finally:
            if conn != None:
                conn.close()


if __name__ == "__main__":

    logging.debug ("main in gs.py")

    g = GSU()


    while True:
        dp1 = random.randrange (-10, 40)
        dp2 = random.randrange (0, 100)

        g.sendData ({ 'compId': 'GreenEyeMonitor', 'dp1' : dp1, 
                      'dp2' : dp2})

        time.sleep(10)

