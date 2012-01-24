import socket
import os
import time
import sys
import urllib2
import random
from qoutes import qoutes

bot_version="0.6"

class connection():

	nick = "dragonBot"
	realname = nick
	ident = nick
	channel = "#raspberrypi-bots"
	nickList = []
	away = True

	def __init__(self, address):
		self.address = address
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		self.sock.connect((socket.gethostbyname(address), 6667))
		self.sock.send("USER %s %s %s :%s\r\n" % (self.ident, address, "UNIX-SERVER", self.realname))
		self.sock.send("NICK %s\r\n" % (self.nick))
		self.sock.send("JOIN %s\r\n" % (self.channel))
	def server_response(self):
		response = self.sock.recv(1024)
		if "PING :" in response[:7] and "PRIVMSG" not in response:
			self.sock.send( response.replace("PING", "PONG" ))
			return 0
		if "!" in response and ":" in response[response.index(":") + 1:]:
			return response
	def send_message(self, message):
		if not message:
			return False
		if self.channel:
			message_tuple = ( self.nick, self.ident, self.address, self.channel, message)
			return self.sock.send(":%s!%s@%s PRIVMSG %s :%s\r\n" % message_tuple)
	def parse_message(self, message):
		nick = message[message.index(":"):message.index("!")]
		if nick not in self.nickList:
			self.nickList.append(nick)
		message = message[message.index(":")+1:]
		message = message[message.index(":"):]
		return "%s %s" % (nick, message)
	def close(self):
		self.sock.close()


def google(search):
	print("Heh")

nick = ""
connected = True
server = connection( "irc.freenode.net" )
#execfile("faqs_qoutes")
qouteDict = {
	"are they for sale yet":"Not yet, but hold on because it's not going to be much longer. ;)",
	"can I buy one yet":"Not yet, but hold on because it's not going to be much longer. ;)",
	"when can I buy a raspberry pi":"Likely later in January or early Febuary. Keep an eye on the store, http://www.raspberrypi.com, and subscribe to the mailing list.",
	"when can I buy one":"Likely later in January or early February. Keep an eye on the store!",
	"where can I buy a raspberry pi":"From the raspberry pi store, of course, after it's released, at http://www.raspberrypi.com.",
	"will it run windows":"Currently no, and likely not in the foreseeable future, due to the limited resources and the processor achetecture. Feel free to take a look around linux!",
	"can it run crysis on max":"Of course, and it also flies and plays folky drum and bass.",
	"how much is a raspberry pi":"Model A will be $25, a model B will be $35. This is of course not including any peripherals."
	}
#qouteDict = qoutes.qoutesDict
trustedNicks = [ "mrdragons" ]
ignoreList = []

if os.path.exists("qoutes"):
	exec(compile(open("qoutes").read(), "qoutes", 'exec'))
else:
	qoutesFile=open("qoutes", "w")

randomKill = str(random.randint(1,1000))
print("Random kill code is %s" % randomKill)
try:
	while connected:
		counter = 0
		response = server.server_response()
		if response:
			print(response)
			message = server.parse_message(response.lower())
			messageRay = message.split(" ")

			action = [ ]
			
			for thing in messageRay[1:]:
				action.append(thing.strip(":"))
				counter+=1
			while counter < 6:
				action.append(" ")
				counter+=1
			nick = messageRay[0].strip(":")
			nick = nick.lower()
			bot_nick = server.nick
			bot_nick = bot_nick.lower()
			
			sensitivity = 2

			print(qouteDict)
			if server.away == False and nick not in ignoreList and bot_nick in message and len(messageRay)>2: 
				if "kill " + bot_nick in message and randomKill in message:
					server.close()
				elif "hello " + bot_nick in message or "hey " + bot_nick in message or "hi " + bot_nick in message:
					server.send_message("Hello %s! This is %s v%s." % (nick, bot_nick, bot_version))
				elif "what's the time" in message or "what time is it" in message:
					server.send_message("%s: Adventure time! (And %s.)" % ( nick, time.strftime("%A, %B %d, %H:%M EST")))
				elif "go away" in message and bot_nick in message or "shut up" in message and bot_nick in message:
					server.away = True
					server.send_message("Ok, just tell me when to come back.")
				elif "ignore me" in message and bot_nick in message:
					ignoreList.append(nick)
					server.send_message("%s: Okay, I'm now ignoring your posts." % nick )
				elif bot_nick in messageRay[1] and "remember" in messageRay[2] and "=" in message:
					if nick in trustedNicks:
						findPos = message.find("=")
						startPos = len(messageRay[0]) + 2 + len(messageRay[1]) + 1 + len(messageRay[2])
						qouteDict.update({message[startPos:findPos].strip(" "):message[findPos+1:len(message)-2].strip(" ")})
						server.send_message("Okay, I'll remember that.")
						qoutesFile=open("qoutes", "w")
						qoutesFile.write("qouteDict= "+ str(qouteDict) +"\ntrustedNicks=" + str(trustedNicks))
						qoutesFile.close()
					else: 
						server.send_message("%s: I don't trust you. >_>" % messageRay[0].strip(":"))
				elif bot_nick in messageRay[1] and "forget" in messageRay[2]:
                                        if nick in trustedNicks:
                                                startPos = len(messageRay[0]) + 2 + len(messageRay[1]) + 1 + len(messageRay[2])
						try:
	                                                qouteDict.pop(message[startPos:-2])
	                                                server.send_message("\x01ACTION forgets that.\x01")
							qoutesFile=open("qoutes", "w")
							qoutesFile.write("qouteDict= "+ str(qouteDict) +"\ntrustedNicks=" + str(trustedNicks))
							qoutesFile.close()
						except KeyError:
							server.send_message("I don't know that.")
                                        else:
                                                server.send_message("%s: I don't trust you. >_>" % messageRay[0].strip(":"))
				elif bot_nick in message[1:] and "add trusted nick" in message and '\"' in message:
					if nick in trustedNicks:
						startPos = message.find('\"')+1
						trustedNicks.append(message[startPos:-3])
						print(trustedNicks)
						qoutesFile=open("qoutes", "w")
	                                        qoutesFile.write("qouteDict= "+ str(qouteDict) +"\ntrustedNicks=" + str(trustedNicks))
        	                                qoutesFile.close()
						server.send_message("User added successfully.")
					else:
						server.send_message("I don't trust you. >_>")
				elif "fuck" in message and bot_nick in message:
					server.send_message("%s: Only if you bring your own condoms." % nick )
				elif "reload qoutes" in message:
					if nick in trustedNicks:
						exec(compile(open("qoutes").read(), "qoutes", 'exec'))
						server.send_message("Qoutes reloaded successfully.")
					else:
						server.send_message("I don't trust you. >_>")
                                elif len(messageRay) > 1:
                                        mostSimilar = 100
                                        sendQoute = "test"
                                        for qoute in qouteDict:
                                                counter=0
                                                similarity=0
                                                qouteRay= qoute.split(" ")
                                                for word in qouteRay:
                                                        if word in message:
                                                                similarity += 1
                                                        counter+=1
                                                #if counter-similarity < len(qouteRay)/2:
                                                if counter-similarity+1 < mostSimilar:
                                                        mostSimilar = counter-similarity
                                                        sendQoute = qoute
                                        
                                        if mostSimilar < len(qouteRay)/2:
                                        	sendQoute = qouteDict[sendQoute]
                                        	sendQoute = sendQoute.replace("{nick}", nick)
                                        	sendQoute = sendQoute.replace("{n}", "\r\n")
                                        	sendQoute = sendQoute.replace("{action 1}", action[0])
                                        	sendQoute = sendQoute.replace("{action 2}", action[1])
                                        	sendQoute = sendQoute.replace("{action 3}", action[2])
                                        	sendQoute = sendQoute.replace("{action 4}", action[3])
                                        	sendQoute = sendQoute.replace("{action 5}", action[4])
                                        	sendQoute = sendQoute.replace("{action 6}", action[5])
                                                server.send_message("%s" % (sendQoute))

			if "come back" in message and bot_nick in message:
				server.send_message("I'ma back")
				server.away = False
			elif "listen to me" in message and bot_nick in message and nick in ignoreList:
                                ignoreList.remove(nick)
                                server.send_message("%s: Okay, now I'm listening to you." % nick )

except KeyboardInterrupt:
	server.close()
	print("Exitted.")

