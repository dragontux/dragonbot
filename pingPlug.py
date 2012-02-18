import time
from IPC import botIPC_Thread
botIPC = botIPC_Thread()
botIPC.start()

class Plugin:
	handeler     = "ping:"
	shellHandeler = "ping"
	method = "args"
	help   = "Module initially intended for testing, provides some basic info on the bot."

	def ircPlug(nick, message, mtime, channel):
		uptime = 0
		endTime = time.time()
		if botIPC.getVal("pingStartTime") == -1:
			botIPC.setVal("pingStartTime", time.time())
		
		secs = int( endTime - botIPC.getVal("pingStartTime"))
		minutes = int( secs/60    )
		hours   = int( minutes/60 )
		days    = int( hours/24   )
			
		minutes = minutes % 60
		hours   = hours   % 24
		uptime  = ("%d days, %d hours and %d mins" % ( days, hours, minutes ))
		return ("%s: Pong, bot nick is: %s, logs on: %s, no. of plugins loaded: %d, uptime: %s" % (nick, 
													botIPC.getVal("botNick"), 
													botIPC.getVal("logsOn"), 
													len(botIPC.getVal("plugins")), uptime))
	def shellPlug(args):
		print("You gave the args %s." % args)
