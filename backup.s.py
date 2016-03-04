#!/usr/bin/env python

import socket
import time
import select
import json
import sys
import struct
import signal
from array import *
from Mcaster import *

class powerusage(object):

    def __init__ (self):
        self.aValues = [None]*64
        self.total = 0

        self.temp1 = 0.0
        self.temp2 = 0.0
        self.temp3 = 0.0
        self.temp4 = 0.0
        self.temp5 = 0.0

        for i in range(0,64):
            self.aValues[i] = 0


    def config(self):
        pass

    def connect(self):
   
        self.s = tcpSocket()
        self.s.connect ("10.0.69.8", 2101)

        self.mc = Mcaster ("239.139.0.2", 5000, 1)


    def parse (self, v):

        # we are passed like a1=22

        s = v.split("=")
        i = int(s[0][2:len(s[0])])
        n = int(s[1])

        print "i = %d n = %d" % (i, n)
        self.aValues[i] = n

    def calculate(self):

        self.total = self.aValues[3] + self.aValues[6]

    def writeCactiFile(self):

        
        s = ""
        for i in range (1,32):
            ns = "p%d:%d " % (i, self.aValues[i])
            s = s + ns

        s = s + "total:%d\n" % (self.total)

        of = open ("/tmp/gemdata", "w")
        of.write (s)
        of.close()


    def dump(self):

        self.calculate()

        # clear the screen
        print chr(27) + "[2J"
        print chr(27) + "[H"

        print "Temp1=%2.1f Temp2=%2.1f Temp3=%2.1f Temp4=%2.1f" % (
            self.temp1, self.temp2, self.temp3, self.temp4)

        print "Total Power = %d W" % self.total
        print "                  L1  %03d" % self.aValues[1]
        print "                  L2  %03d" % self.aValues[2]

        for i in xrange(3,31,2):
            print "   L%2d  %03d       L%2d  %03d" % (i,self.aValues[i], i+1, self.aValues[i+1])

    def getJsonString(self):

        data = [ self.total, self.aValues, self.temp1, self.temp2, self.temp3, self.temp4]

        jsonString = json.dumps (data)
        return jsonString

    def setJsonString(self, s):

        [self.total, self.aValues, self.temp1, self.temp2, self.temp3, self.temp4] = json.loads (s)



    def interactWithGEM(self):


        # First, lets see if we can get some data from the other side
        rlist, wlist, elist = select.select ([self.s.sock], [], [], 5)

        if len(rlist) == 0:
            #            print "we should poll the device!"
            #            print "%c[2J" % (27)
            print "Polling!"
            self.s.send("^^^APIVAL")

        else:
            r = self.s.get()
            if len(r) > 0:
                print "Received: ", r
                self.cs = self.cs + r
                if "\n" in r:


#                    print "there is a new line in there"
#                    print "the full string is ", self.cs

                    i = 1
                    vl = self.cs.split(",")
                    for v in vl:
                        if v.startswith("VAL"):
                            v = v[3:len(v)]

                        print "i = %d v=%s" % (i, v)

                        if v[0].isdigit():


                            if i == 49:
                                self.temp1 = float(v)
                            elif i == 50:
                                self.temp2 = float(v)
                            elif i == 51:
                                i = i
                            elif i == 52:
                                i = i
                            else: 
                                try:
                                    n = int((v))
                                    self.aValues[i] = n
                                
                                except:
                                    i = i

                                    self.aValues[i] = 0
                        

                        i = i + 1
                        
#                        if v.startswith ("p_"):
#                            self.parse(v)
#                            self.dump()

                    self.cs = ""
                    self.sendEveryone()



    def sendEveryone(self):
#        self.dump()
        s = self.getJsonString()
        self.mc.send(s)
        self.writeCactiFile()

    def run(self):

# States
# INIT = 0
# CONNECTING = 1
# RUNNING = 2
# ERROR = 3
# QUIT = 99

        state = 0
        connectingErrorTime = 0
        error = 0

        self.cs = ""

        while state != 99:

            if state == 0:
                self.config()
                state = state + 1
            elif state == 1:

                if connectingErrorTime  == 0:
                 
                    try:

                        self.connect()
                        state = state + 1
                        error = 0

                    except: 

                        if error != 1:
                            print "Some error connecting to server. waiting another 60 seconds"
                            error = 1
                        connectingErrorTime = time.time() + 60
                        time.sleep(60)
                        
                else:

                    if time.time() > connectingErrorTime:
                        connectingErrorTime = 0
                    
                    
                    
            elif state == 2:
               try:
                   self.interactWithGEM()
               except socket.error as serr:
                   state = 3

            elif state == 3:
                self.disconnect()
                state = 1

    def disconnect(self):
        self.s.disconnect()

    def shutdown(self):
        print "Shutting down!"
        self.disconnect()

        


class tcpSocket(object):


    def __init__ (self, sock=None):
        if sock is None:
            self.sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

        else:
            self.sock = sock

    def connect (self, host, port):
        self.sock.connect ((host, port))
#        self.sock.setblocking(0)

    def disconnect (self):
     #   self.sock.shutdown(SHUT_RDWR)
        self.sock.close()

    def send (self, msg):
        self.sock.send (msg)

    def get (self):

        data = None

#        try:

        data = self.sock.recv (2048)
        
#        except:

#            self.disconnect()
#            self.connect()


        return data



def signalHandler (signal, frame):
    print "Signal received"
    pu.shutdown()
    sys.exit(0)


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signalHandler)

    pu = powerusage()
    pu.run()



    





        
            


        
        
        





        
