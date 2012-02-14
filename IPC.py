#!/bin/python3
# For storing variables outside classes, particularly the plugin classes
# This is virtually necessary for using a structure like I did
# Or at least is the slightly more sane solution

import threading
import time

class botIPC_Thread( threading.Thread ):
	joinedChannel = False
	logsOn = False
	botOn = False
	botNick = ""
	channels = []
	plugins = []
	def run(self):
		while True:
			time.sleep(1)
			#Might as well sleep because we're not going to be doing anything.
