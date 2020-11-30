#!/usr/bin/env python

from array import *
#from Mcaster import *
#from s import *

if __name__ == "__main__":
#n	m = McasterReceive ("239.139.0.2", 5000)
#	p = powerusage()

	f = open ("/tmp/gemdata", "r")

	s = f.read()

	ss = s.split(" ")


	print "Content-type: text/xml\n"

	print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
	print "<data>"


	for v in ss:
		ss2 = v.split(":")
		name = ss2[0]
		value = ss2[1]
		
		print "<%s> %s </%s>" % (name, value, name)


#	s = m.get()
	s = s[:-1]
#	p.setJsonString(s)



	print "</data>"
	






        



    





        
            


        
        
        





        

