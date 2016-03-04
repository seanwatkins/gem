#!/usr/bin/env python

import time
import struct
import socket
import sys





class Mcaster():

    def __init__(self, group, port, ttl):
        self.group = group
        self.port = port
        self.addrinfo = socket.getaddrinfo (group, None)[0]
        self.s = socket.socket(self.addrinfo[0], socket.SOCK_DGRAM)
        ttl_bin = struct.pack ('@i', ttl)
        self.s.setsockopt (socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
#        print "Mcaster:: init!"

    def send(self, data):
#        print "Mcaster:: sending '%s'\n " % data
        r = self.s.sendto (data + '\0', (self.addrinfo[4][0], self.port))
#        self.s.send (data)
#        print "Return = %d" %r

class McasterReceive():

    def __init__(self, group, port):
        self.group = group
        self.port = port
        addrinfo = socket.getaddrinfo (group, None)[0]
        self.s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
        self.s.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind (('', self.port))

        group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
        if addrinfo[0] == socket.AF_INET:
            mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
            self.s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def get (self):
        return self.s.recv(1500)
        
        


def testit():

        a1 = 1
        a2 = 2
        a3 = 3
        a4 = 4
        a5 = 5
        a6 = 6
        a7 = 7
        a8 = 8
        a9 = 9
        a10 = 10
        a11 = 11
        a12 = 12
        a13 = 13
        a14 = 14
        a15 = 15
        a16 = 16
        a17 = 17
        a18 = 18
        a19 = 19
        a20 = 20
        a21 = 21
        a22 = 22
        a23 = 23
        a24 = 24

        data = "TedData %5.4f %5.4f %5.4f %5.4f %5.4f %5.4f %5.4f %5.4f %5.4f %5.4f %5.4f %5.4f %s %5.4f %4s %5.4f %d %5.4f %d %5.4f %5.4f %5.4f %5.4f %5.4f" %  (a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24 )


        return data


def main():
    group = "239.139.0.2"
    port = 5000
    m = Mcaster(group, port, 2)
    mr = McasterReceive(group, port)


    while True:
#       m.send("hey fag")
 #      print "sent"
       s = mr.get()
       print "received: ", s
        


if __name__ == '__main__':
    main()


                 





    