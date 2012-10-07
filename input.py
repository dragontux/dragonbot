import irc
import threading

class in_thread( threading.Thread ):
	def __init__( self, server, p_man ):
		threading.Thread.__init__(self)
		self.server = server;
		self.p_man  = p_man

	def run( self ):
		server = self.server
		while True:
			response = server.recv()
			lines	= response.split("\n");
			if len( response ) < 4:
				exit( 0 )
			else:
				pass
				#print( response )
				
			for line in lines:
				if "PING :" in line[0:7]:
					server.send( line.replace( "I", "O", 3 ))
					print( "-----[ Sent pong ]-----" )
				elif "PRIVMSG" in line:
					parsed = irc.parse_message( line );
				
					if parsed:
						if parsed["channel"][0] == "#":
							reply_to = parsed["channel"]
						else:
							reply_to = parsed["nick"]
						#print( "[debug] got: %s: %s" % ( reply_to, parsed["message"] ))
						if parsed["message"][0] == "!":
							self.p_man.exec_cmd( parsed )
