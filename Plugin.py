class Plugin:
	handeler     = "plugin test"
	shellHandeler = "pluginTest"
	method = "string"

	def __init__(self, connection):
		self.message = ""
		self.nick = ""
		self.inittime = ""
		self.connection = connection
	def ircPlug(nick, message, time, channel):
		return ("You posted %s at %s to %s." % ( message, time, channel ))
	def shellPlug(args):
		print("You gave the args %s." % args)
