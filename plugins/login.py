import time

class plugin:
	handle	= "login"
	method	= "args"
	do_init = False;
	cron_time = False;
	passfile = "bot_passwd"

	def in_passfile( self, nick, password ):
		try:
			fp = open( self.passfile, "r" )
		except IOError as e:
			print( "password file error:", e )
			return False

		buf = fp.readline()
		while len( buf ) > 0:
			key = buf.split()
			if ( len( key ) > 1 ):
				if nick == key[0] and password == key[1]:
					return True
			buf = fp.readline()
		return False
	
	def run( self, pman, server, nick, channel, args ):
		if channel[0] == "#": 	reply_to = channel
		else:			reply_to = nick
		msg = ""
		nicks = pman.get_trusted()

		if len( args ) < 2:
			msg = "Need args: [action] [pass]"
		else:
			if args[1] == "login":
				if nick in nicks:
					msg = "You are already logged in!"
				elif len( args ) < 3:
					msg = "Need args: login [password]"
				elif self.in_passfile( self, nick, args[2] ):
					pman.add_trusted( nick )
					msg = "You are now logged in."
				else:
					msg = "Invalid username/password."
			elif args[1] == "logout":
				if nick in nicks:
					pman.remove_trusted( nick )
					msg = "You are now logged out."
				else:
					msg = "You are not logged in."
			else:
				msg = "Unknown action \"" + args[1] + "\""

		server.send_message( reply_to, msg );
