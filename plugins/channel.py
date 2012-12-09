import string
class plugin:
	handle    = "bot"
	method 	  = "args"
	do_init   = True
	cron_time = False

	def init( self ):
		print( "        Plugin initialised" )
	def run( self, pman, server, nick, channel, args ):
		if channel[0] == "#": 	reply_to = channel
		else: 			reply_to = nick
		msg = False

		nicks = pman.get_trusted();

		if nick in nicks:
			if len( args ) > 2:
				if args[1] == "join":
					server.join( args[2:] )
					msg = "Joined channels " + str( args[2:] )
				elif args[1] == "part":
					server.part( args[2:] )
					msg = "parted channels " + str( args[2:] )
				elif args[1] == "quit":
					server.quit( " ".join( args[2:] ))
				elif args[1] == "say":
					if len( args ) > 3:
						reply_to = args[2]
						msg = " ".join( args[3:] )
					else:
						msg = "Need arguments."
				elif args[1] == "nick":
					server.nick( args[2] )
					msg = False
				else:
					msg = "Unknown command."
			else:
				msg = "Need arguments"
		else:
			msg = "You are not authorized to use the bot."

		if msg:
			server.send_message( reply_to, msg );
