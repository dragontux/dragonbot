import os

if os.path.exists("qoutes"):
	exec(compile(open("qoutes").read(), "qoutes", 'exec'))
else:
	qoutesFile=open("qoutes", "w")
	qouteDict = {}
	trustedNicks = [ "mrdragons" ] 

handeler = "q:"

def saveQoutes():
	qoutesFile = open("qoutes", "w")
	qoutesFile.write( "qouteDict=" + str(qouteDict) + "\ntrustedNicks=" + str(trustedNicks))
	qoutesFile.close()
	return 1


class Plugin:
	handeler = handeler
	method = "string"
	def __init__(self):
		self.message = ""
		self.nick = ""
		self.inittime = ""
		self.connection = connection
	def ircPlug( nick, message, time, channel):
		message = message.lower()
		message = message[len(handeler):]
		messageRay = message.split(" ")
		messageRay = messageRay[2:]
		print(messageRay)
		nick = nick.lower()
		#print(messageRay)
		if "hello bot" in message:
			return ("Hello there " + nick + ".")
		elif "remember" in message and "=" in message:
			if nick in trustedNicks:
				print("Okay, we got here...")
				findPos = message.find("=")
				startPos = len(messageRay[0]) + len(messageRay[1]) + 3
				qouteDict.update({message[startPos:findPos].strip(" "):message[findPos+1:].strip(" ")})
				return ("Okay, I'll remember that.")
				qoutesFile = open("qoutes", "w")
				qoutesFile.write( "qouteDict=" + str(qouteDict) + "\ntrustedNicks=" + str(trustedNicks))
				print(qoutesFile.read())
				qoutesFile.close()
			else:
				return "I don't trust you. >_>"
		elif "reload qoutes" in message:
			if nick in trustedNicks:
				exec(compile(open("qoutes").read(), "qoutes", 'exec'))
				return ("Qoutes reloaded.")
			else:
				return ("I don't trust you. >_>")
		elif "add" in messageRay[0]:
			if "trusted" in messageRay[1] and "nick" in messageRay[2]:
				if nick in trustedNicks:
					trustedNicks.append(messageRay[3].lower())
					if saveQoutes() == 1:
						return ("Nick %s added to trusted users." % ( messageRay[3] ) )
					else:
						return "Hmm... There may have been an error saving the file, try again."
				else:
					return "I don't trust you. >_>"
		elif "remove" in messageRay[0]:
			if "trusted" in messageRay[1] and "nick" in messageRay[2]:
				if nick in trustedNicks:
					try:
						trustedNicks.remove(messageRay[3])
						if saveQoutes() == 1:
							return ("Nick %s removed from trusted users." % ( messageRay[3] ))
						else:
							return ("There was an error accessing the data file. Try again in a moment.")
					except ValueError as e:
						return ("Nick %s does not exist." % ( messageRay[3] ))
				else:
					return "I don't trust you. >_>"
		elif len(messageRay) > 1:
			mostSimilar = 100
			sendQoute = "test"
			for qoute in qouteDict:
				counter = 0
				similarity = 0
				qouteRay = qoute.split(" ")
				for word in qouteRay:
					if word in message:
						similarity += 1
					counter+=1
				if counter-similarity < mostSimilar:
					mostSimilar = counter-similarity
					sendQoute = qoute
			if mostSimilar < len(qouteRay)/2:
				sendQoute = qouteDict[sendQoute]
				return sendQoute
