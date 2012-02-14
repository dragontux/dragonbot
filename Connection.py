#!/bin/python3

import socket

class ircServer():
	channelList = [ ]
	address = ""
	nick = ""

	def __init__(self, address, channels, bot_nick ):
		self.nick = bot_nick
		self.ident = self.nick
		self.realname = self.nick

		self.address = address
		self.channelList = channels

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((socket.gethostbyname(address), 6667))
		print("Connected to server")

		sendStr = "USER %s %s %s :%s\r\n" % (self.ident, address, "UNIX-SERVER", self.realname)
		self.sock.send(bytes(sendStr, 'UTF-8'))
		self.sock.send(bytes("NICK %s\r\n" % self.nick , 'UTF-8'))
		for channel in self.channelList:
			self.sock.send(bytes("JOIN %s\r\n" % channel, 'UTF-8'))
		print("Joined channels " + str(self.channelList) + ".")
		
	def server_response(self):
		response = str(self.sock.recv(1024))
		if "PING :" in response and "PRIVMSG" not in response:
			self.sock.send( bytes(response.replace("PING", "PONG"), 'UTF-8'))
			return 0
		if "!" in response and ":" in response[response.index(":") + 1:]:
			return ( response, response.split(" ") )
	def send_message( self, message, channel ):
		if not message:
			return False
		if len(self.channelList) > 0:
			return self.sock.send(bytes( ":%s!%s@%s PRIVMSG %s :%s\r\n" % ( self.nick, self.ident, self.address, channel, message ), 'UTF-8'))
	def raw_message( self, message ):
		if not message:
			return False
		else:
			return self.sock.send(bytes(message, 'UTF-8'))
	def parse_message(self, message):
		message = str(message)
		try:
			nick = message[message.index(":")+1:message.index("!")]
			message = message[message.index(":")+2:-5]
			message = message[message.index(":")+1:]
			return "%s %s" % ( nick, message ) 
		except ValueError:
			return 0
	def close(self):
		self.sock.close()
