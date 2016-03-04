#!/usr/bin/env python

from array import *
from Mcaster import *
from s import *


if __name__ == "__main__":
    m = McasterReceive ("239.139.0.2", 5000)
    p = powerusage()

    while 1:
        s = m.get()
        s = s[:-1]
#        print "String is '%s'" % s
        p.setJsonString(s)
        p.dump()





        



    





        
            


        
        
        





        

