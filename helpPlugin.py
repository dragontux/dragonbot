class Plugin:
	handeler      = "help:"
	shellHandeler = "helpPlug"
	method        = "args"
	def ircPlug(nick, args, time, channel):
		helpDict      = { 
			"q:"   : "Ask a question, if a similar question has been answered and stored before it will reply with an answer.",
			"help": "Get help for one of the standard bot modules.",
			"drop:": "Picks a random link from previous chats and returns it, can find some really cool things."
		}
		if len(args) == 1:
			return (nick + ": Standard commands: %s" % (list(helpDict.keys())))
		elif len(args) >= 2 and args[1] in helpDict:
			return (helpDict[args[1]])
		else:
			return ("I don't have any help for that, sorry. :(")
	def shellPlug(args):
		print("You gave the args %s." % args)
