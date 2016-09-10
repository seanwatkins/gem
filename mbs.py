#!/usr/bin/env python
# ModBus Server

from pymodbus.server.sync import StartTcpServer
from pymodbus.server.sync import StartUdpServer
from pymodbus.server.sync import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

import threading
import time
import datetime
import os
import signal

from Mcaster import *

from s import *




#from pymodbus.transaction import ModbusRtuFrame

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

store = ModbusSlaveContext(
	ir = ModbusSequentialDataBlock(0, [9999]*100)) # input register - 16 bit 

context = ModbusServerContext(slaves=store, single=True)

#---------------------------------------------------------------------------# 
# initialize the server information
#---------------------------------------------------------------------------# 
# If you don't set this or any fields, they are defaulted to empty strings.
#---------------------------------------------------------------------------# 
identity = ModbusDeviceIdentification()
identity.VendorName  = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl   = 'http://github.com/bashwork/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName   = 'Pymodbus Server'
identity.MajorMinorRevision = '1.0'


class myThread (threading.Thread):

	def __init__ (self, threadID):
		threading.Thread.__init__(self)
		self.threadID = threadID

	def run(self):

		# Setup to Receive multicast packets
		m = McasterReceive ("239.139.0.2", 5000)
		p = powerusage()

		while True:
			
			# wait for multicast json string
			s = m.get()
			s = s[:-1]
			p.setJsonString(s)

			register = 0x3
			slave_id = 0x1
			address = 0x00

			now = datetime.datetime.now()

			values   = context[slave_id].getValues(register, address, count=100)

			values[0] = now.hour
			values[1] = now.minute
			values[2] = now.second

			values[10] = int (p.temp1 * 1000)
			values[11] = int (p.temp2 * 1000)
			values[12] = int ( p.temp3 * 1000)
			values[13] = int (p.temp4 * 1000)

			t =int( p.aValues[3] + p.aValues[6])
			values[20] = t

			for i in range (1, 32):
				x = int(p.aValues[i])
				values[30+i] = x
#				print "%d %d" % (30+i, x)

#			print values

			context[slave_id].setValues(register, address, values)





thread1 = myThread(1)

thread1.start()





# Tcp:
StartUdpServer(context, identity=identity, address=("10.0.69.13", 5020))

