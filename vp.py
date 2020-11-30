#!/usr/bin/env python

from array import *
from Mcaster import *
from s import *

class breaker(object):
    
    def __init__ (self):
        self.no = -1
        self.watts = 0
        self.description = "Unknown"
        self.type = 0 # 0 - unknown, 1 active, 2 ignore
        

    def __str__ (self):
        s = "Breaker %d Description %s Watts %s Type %d" % (self.no,
                                                    self.watts,
                                                    self.description,
                                                    self.type)
                                                  
        return s

    def __repr__ (self):
        return self.__str__()

    def active (self):
        self.type = 1

    def ignore (self):
        self.type = 2

    



class breakerpanel (object):

    def __init__ (self):
        self.noBreakers = 0
        self.breakers = None
        self.totalWatts = 0.0

    def setBreakers (self, n):
        self.noBreakers = n
        self.breakers = None
        self.breakers = [breaker()] * (n+1)

        for i in xrange (1,n+1,1):
            b =  breaker()
            b.no = i
            self.breakers[i] = b


    def init(self):
        self.setBreakers(32)

        for i in xrange(1, self.noBreakers+1, 1):
            self.breakers[i].type = 1

        self.breakers[1].description = "Panel Recp"
        self.breakers[2].description = "HWT"
        self.breakers[3].description = "Left Side"
        self.breakers[4].description = "Bedroom"
        self.breakers[5].description = "Microwave"
        self.breakers[7].description = "Wall Oven"
        self.breakers[8].description = "Basement Bedroom"

        self.breakers[10].description = "Master Bedroom"
        self.breakers[11].description = "Counter Recep"
        
        self.breakers[12].description = "Lights"
        self.breakers[14].description = "Lights"
        self.breakers[19].description = "Kitchen Table"
        self.breakers[20].description = "Dishwasher"
        self.breakers[21].description = "Living Room"
        self.breakers[22].description = "Dryer"
        self.breakers[23].description = "Basement Theatre"
        self.breakers[25].description = "Lights"
        self.breakers[26].description = "Computers"
        self.breakers[27].description = "Living Room"                
        self.breakers[28].description = "Furnace"
        self.breakers[29].description = "Fridge"
        self.breakers[30].description = "Bedroom Upstairs South"
        self.breakers[31].description = "Lights"
        self.breakers[32].description = "Lights"

        
        
        self.breakers[3].type = 2
        self.breakers[6].type = 2
        
    def dump(self):

        print "Panel Dump"
        print "# of Breakers %d " % self.noBreakers
        print "Total Watts %d" % self.totalWatts
        
        for i in xrange (1, self.noBreakers+1, 1):
                print self.breakers[i]


    def calcTotalUsage(self):
        self.totalWatts = self.breakers[3].watts  + self.breakers[6].watts

    def setAllUsage (self, a):

#        print "setAllUsage: %s" % a
#       print "NoBreakers %d " % self.noBreakers
        
       for i in xrange (1,self.noBreakers+1,1):
           v = a[i]
 #          print "i=%d v=%d\n" % (i, v)
           self.breakers[i].watts = v
#           print self.breakers[i]

    def sortedUsage(self):

        self.sortedBreakers = sorted (self.breakers, key=lambda breaker: breaker.watts, reverse=True)
                


if __name__ == "__main__":
    m = McasterReceive ("239.139.0.2", 5000)
    p = powerusage()

    bp = breakerpanel()
    bp.init()
#    bp.dump()


    while 1:
        s = m.get()
        s = s[:-1]
#        print "String is '%s'" % s
        p.setJsonString(s)
#        p.dump()

        l = p.aValues

        bp.setAllUsage (l)

        # calculate total
        bp.calcTotalUsage()
        bp.sortedUsage()

        print "Basement=%2.1f Main=%2.1f Upstairs=%2.1f Outside=%2.1f" % (
            p.temp1, p.temp3, p.temp2, p.temp4)


        print "Total Watts = %d" % (bp.totalWatts)

  #      td = 0.0



        for i in xrange(1, 32+1,1):


            if (bp.sortedBreakers[i].type == 1):
                v = bp.sortedBreakers[i].watts
                n = bp.sortedBreakers[i].no
                d = bp.sortedBreakers[i].description
                print "L%2d %03dW %-15s " % (n, v, d)

#                td = td + p


 #       print "Total Monthly $%3.2f" % td
        print "\n"
        






        



    





        
            


        
        
        





        

