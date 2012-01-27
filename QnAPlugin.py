import os

if os.path.exists("qoutes"):
	exec(compile(open("qoutes").read(), "qoutes", 'exec'))
else:
	qoutesFile=open("qoutes", "w")
	qouteDict = {}

trustedNicks = [ "mrdragons" ] 
handeler = "q:"

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
		if "hello bot" in message:
			return ("Hello there " + nick + ".")
		elif "remember" in message[2] and nick in trustedNicks and "=" in message:
			findPos = message.find("=")
			startPos = len(messageRay[0]) + len(messageRay[1] + 3)
			qouteDict.update({message[startPos:findPos].strip(" "):message[findPos+1:len(message)-2].strip(" ")})
			return ("Okay, I'll remember that.")
			qoutesFile = open("qoutes", "w")
			qoutesFile.write( "qouteDict=" + str(qouteDict) + "\ntrustedNicks=" + str(trustedNicks))
		elif "reload qoutes" in message and nick in trustedNicks:
			exec(compile(open("qoutes").read(), "qoutes", 'exec'))
			return ("Qoutes reloaded.")
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
