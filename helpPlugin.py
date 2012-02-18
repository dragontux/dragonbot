from IPC import botIPC_Thread
botIPC = botIPC_Thread()
botIPC.start()

class Plugin:
	handeler      = "help:"
	shellHandeler = "help"
	method        = "args"
	help          = "Gives help for a bot module or command."
	def ircPlug(nick, args, time, channel):
		#helpDict      = { 
		#	"q:"   : "Ask a question, if a similar question has been answered and stored before it will reply with an answer.",
		#	"help": "Get help for one of the standard bot modules.",
		#	"drop:": "Picks a random link from previous chats and returns it, can find some really cool things."
		#}
		helpDict = {}
		tempPlugins = botIPC.getVal("plugins")
		for plug in tempPlugins:
			try:
				helpDict.update({plug.Plugin.handeler:plug.Plugin.help})
			except Exception:
				pass
		if len(args) == 1:
			return (nick + ": Standard commands: %s" % (list(helpDict.keys())))
		elif len(args) >= 2 and args[1] in helpDict:
			return (helpDict[args[1]])
		else:
			return ("I don't have any help for that, sorry. :(")
	def shellPlug(args):
		print("Bot help module")
		print("Standard commands:\n")
		print("\tmodules \vUsage: modules \n\t\tLists loaded modules")
		print("\tplugins \vUsage: plugins \n\t\tSame as modules")
		print("\tunload  \vUsage: unload [module number] \n\t\tUnloads a module\n\t\tNumber can be retrieved from 'modules' or 'plugins'")
		print("\tload    \vUsage: load [module name] \n\t\tLoad a module with the given name")
		print("\tpost    \vUsage: post [channel name] [message] \n\t\tPost a message to a channel from the bot")
		print("\tclear   \vUsage: clear \n\t\tClears the window")
		print("\thelp    \vUsage: help \n\t\tThis help")
		print("\nNote that each plugin may have shell commands that are not listed here.")
