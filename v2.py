#!/usr/bin/env python

from array import *
from Mcaster import *
from s import *

class powerBreaker(object):

    def __init (self):
        self.no = 0
        self.power = 0

    def __init__ (self, no):
        self.no = no
        self.power = 0

    def setPower (self, power):
        self.power = power

    def setNo (self, no):
        self.no = no

    def getNo (self):
        return self.no

    def getPower (self):
        return self.Power
        

if __name__ == "__main__":
    m = McasterReceive ("239.139.0.2", 5000)
    p = powerusage()

    breakerList = {}

    for bNo in range(1,33):

        breakerList[bNo] = 0

    print breakerList

    while 1:
        s = m.get()
        s = s[:-1]

        p.setJsonString(s)
        


        for i in range (1,33):

            breakerList[i] = p.aValues[i]

        
#        for key, value  in sorted(breakerList.items(), key=lambda q: q[key])
#            print key, value

        print breakerList

            


        






        



    





        
            


        
        
        





        

