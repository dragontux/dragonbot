#!/bin/python3

import socket
import os
import time
import sys
import threading
import imp
import botColors
from botColors import printColor
from Connection import ircServer
from IPC import botIPC_Thread

server     = [ "irc.freenode.net", [ "#raspberrypi-bots" ]]
bot_nick   = "dragonTux"
pluginList = [ "Plugin", "QnAPlugin", "logPlugin", "pingPlug", "helpPlugin" ]
execList   = [ ]
connection = ircServer( server[0], server[1], bot_nick )

botIPC = botIPC_Thread()
botIPC.start()
botIPC.setName(bot_nick + "IPC")

botIPC.setVal("botOn", True)
botIPC.setVal("botNick", bot_nick)

for plug in pluginList:
	try:
		plugin = __import__(plug, globals(), locals(), [], -1)
		execList.append(plugin)
		tempList = botIPC.getVal("plugins")
		tempList.append(plugin)
		botIPC.setVal("plugins", tempList)
	except Exception as ie:
		print("Error: " , ie)
		print("Module not loaded.")

class recieveThread( threading.Thread ):
	def run(self):
		while botIPC.getVal("botOn") == True:
			response = connection.server_response()
			if response:
				message = connection.parse_message( response[0] )
				messageArgs = message.split(" ")
				nick = messageArgs[0]
				messageArgs = messageArgs[1:]
				message = message[len(nick)+1:]

				channel = response[1][2]
				curTime = time.strftime("%T")
				if channel != bot_nick:
					tempList = botIPC.getVal("plugins")
					for plug in tempList:
						if plug.Plugin.handeler in messageArgs[0]:
							try:
								if plug.Plugin.method == "string":
									connection.send_message(plug.Plugin.ircPlug(nick, message, curTime, channel), channel)
								elif plug.Plugin.method == "args":
									connection.send_message(plug.Plugin.ircPlug(nick, messageArgs, curTime, channel), channel)
							except Exception as e:
								print("Error! Module %s encountered an error.\nProgram not executed." % (plug), e)
								tempList.remove(plug)
								botIPC.setVal("plugins", tempList)
						else:
							#print("%s" % message[len(messageArgs[0])+1:])
							pass
class shellThread( threading.Thread ):
	def run(self):
		while botIPC.getVal("botOn") == True:
			userInput = input( "%s%s%sShellv0.2 > " % (botColors.colorDict["blue"], bot_nick, botColors.colorDict["endchar"]))
			userArgs = userInput.split(" ")
			returnedTrue = False
			tempList = botIPC.getVal("plugins")
			if userArgs[0] == "load" and len(userArgs) > 1:
				try:
					plugin = __import__(userArgs[1], globals(), locals(), [], -1)
					#execList.append(plugin)
					tempList.append(plugin)
					botIPC.setVal("plugins", tempList)
					printColor("Successfully loaded", "green")
				except Exception as ie:
					print("Error: ", ie)
					printColor("Module not loaded.", "boldred")
			elif userArgs[0] == "unload" and len(userArgs) > 1:
				try:
					imp.reload(tempList[int(userArgs[1])])
					#del execList[int(userArgs[1])]
					del tempList[int(userArgs[1])]
					botIPC.setVal("plugins", tempList)
					printColor("Unloaded.", "green")
				except Exception as e:
					printColor("Error: %s" % ( e ), "boldred")
			elif userArgs[0] == "modules" or userArgs[0] == "plugins":
				counter = 0
				#for item in execList:
				for item in tempList:
					print( "%s%3s%s | %s " % ( botColors.colorDict["green"], counter, botColors.colorDict["endchar"], item ))
					counter += 1
			elif userArgs[0] == "post" and len(userArgs) > 1:
				connection.send_message(userInput[len(userArgs[1])+6:], userArgs[1])
				print("Sent message.")
			elif userArgs[0] == "clear":
				tempVar = os.system("clear")
			elif userArgs[0] == "quit":
				botIPC.setVal("botOn", False)
			else:
				counter = 0
				for plug in tempList:
					counter += 1
					if userArgs[0] == plug.Plugin.shellHandeler:
						try:
							plug.Plugin.shellPlug(userInput[len(userArgs[0])+1:])
							returnedTrue = True
						except Exception as e:
							print("Error! Plug %s: %s" % (plug, e))
					elif returnedTrue == False and counter == len(tempList) and len(userInput) > 0: 
						print("Unknown command. ('help' maybe?)")

try:
	shell    = shellThread()
	getStuff = recieveThread()

	shell.setName( bot_nick + "Shell" )
	getStuff.setName( bot_nick + "Recieve" )

	getStuff.start()
	shell.start()

except KeyboardInterrupt as e:
	connection.raw_message("QUIT :wtfisthiscrap982374")
	print("\nError: ", e)
	botIPC.setVal("botOn", False)
