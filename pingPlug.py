class Plugin:
	handeler     = "ping:"
	shellHandeler = "ping"
	method = "args"

	def ircPlug(nick, message, time, channel):
		return ("%s: Pong" % nick)
	def shellPlug(args):
		print("You gave the args %s." % args)
