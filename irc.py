import socket

def parse_message( message ):
	try:
		channel = message.split()[2]
		nick = message[message.index(":")+1 : message.index("!")]
		message  = message[message.index(":")+2:]
		message  = message[message.index(":")+1:]
		return { "nick":nick, "channel":channel, "message":message }
	except ValueError:
		return False

class irc_server( ):
	def __init__( self, server ):
		self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM );
		self.sock.connect(( socket.gethostbyname( server ), 6667 ))

	def send( self, message ):
		self.sock.send(bytes( message, "UTF-8" ))

	def recv( self ):
		return self.sock.recv( 1024 ).decode()

	def send_message( self, channel, message ):
		self.send( "PRIVMSG %s :%s\r\n" % ( channel, message ))

	def identify( self, nick ):
		self.send( "USER %s %s %s :%s\r\n" % ( nick, nick, nick, nick ))
		self.send( "NICK %s\r\n" % ( nick ))

	def nick( self, nick ):
		self.send( "NICK %s\r\n" % ( nick ))

	def join( self, channels ):
		for thing in channels:
			self.send( "JOIN %s\r\n" % ( thing ))

	def part( self, channels ):
		for thing in channels:
			self.send( "PART %s\r\n" % ( thing ))

	def quit( self, message ):
		self.send( "QUIT :" + message + "\r\n" )
		self.sock.close()
		exit(0)
