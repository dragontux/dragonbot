#!/bin/python3
# For storing variables outside classes, particularly the plugin classes
# This is virtually necessary for using a structure like I did
# Or at least is the slightly more sane solution
# (Slightly (and still more insane than others))

import threading
import time
import os

class botIPC_Thread( threading.Thread ):

	lookupData = { "joinedChannel":0, "logsOn":1, "botOn":2, "botNick":3, "channels":4, "plugins":5 }
	dataList   = [ False, False, False, "", [], [] ]
	id = -1

	def refreshFile(self):
		if os.path.exists("tempBotData"):
			fd = open("tempBotData", "r")
			fileData = fd.read().split("#")
			fd.close()
			#if self.id == -1:
			#	id = int(fileData[0]) + 1
			#if self.id <= int(fileData[0]):
			if True:
				fd = open("tempBotData", "w")
				fd.write("%d#self.dataList=%s#self.lookupData=%s" % ( self.id + 1, str(self.dataList), str(self.lookupData)))
				fd.close()
				return 0
			#elif self.id > int(fileData[0]):
			#	exec(fileData[1])
			#	exec(fileData[2])
			#	return 1
		else:
			fd = open("tempBotData", "w")
			fd.write("%d#self.dataList=%s#self.lookupData=%s" % ( self.id + 1, str(self.dataList), str(self.lookupData)))
			fd.close()

	def getVal(self, lookup):
		if lookup in self.lookupData:
			return self.dataList[self.lookupData[lookup]]
		else:
			return -1

	def setVal(self, valueToSet, value):
		if valueToSet in self.lookupData:
			self.dataList[self.lookupData[valueToSet]] = value
		else:
			self.lookupData.update({valueToSet:len(self.dataList)})
			self.dataList.append(value)

	def run(self):
		while True:
			self.refreshFile()
			time.sleep(3)
