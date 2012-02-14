#!/bin/python3
# The log plugin

import os
from time import strftime
import threading
from IPC import botIPC_Thread

botIPC = botIPC_Thread()
if botIPC.isAlive == False:
	print("IPC off! Logs won't work...")
else:
	class Plugin:
		handeler = ""
		shellHandeler = "log"
		method = "string"

		class logVariables( threading.Thread ):
			on = False
			def run(self):
				pass
		bots = logVariables()
		if botIPC.isAlive == False:
			print("IPC off...")
	
		def ircPlug(nick, message, mtime, channel):
			if botIPC.logsOn == True:
				logName = "log-" + strftime("%m-%d-%y")
				dirName = channel + strftime("%m-%y")
	
				if os.path.exists("log") == False and os.path.isdir("log") == False:
					os.mkdir("log")
				if os.path.exists("log/" + dirName) == False and os.path.isdir("log/" + dirName) == False:
					os.mkdir("log/"+ dirName)

				logFile = open("log/" + dirName + "/" + logName, "a")
				logFile.write("[%s] %s: %s\n" % (mtime, nick, message))
				logFile.close()
		def shellPlug(args):
			shellArgs = args.split(" ")
			if len(shellArgs) >= 1:
				if shellArgs[0] == "on":
					botIPC.logsOn = True
					print("Logs on")
				elif shellArgs[0] == "off":
					botIPC.logsOn = False
					print("Logs off.")
				else:
					print("Que?")
			else:
				print("Need args!")
