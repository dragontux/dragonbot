class plugin:
	handle	= "help"
	method	= "args"
	do_init = False;

	def run( self, pman, server, nick, channel, args ):
		if channel[0] == "#": 	reply_to = channel
		else:			reply_to = nick

		if len( args ) < 2:
			server.send_message( reply_to, nick + ": Loaded plugins: " + str( pman.get_handles( )))
		else:
			server.send_message( reply_to, "I have no help for %s. :(" % ( args[1] ))
