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
	shellHandeler = "QnA"
	method = "string"
	help = "Ask a question in plain english, and if a similar question has been asked and stored before it will reply with an answer. In general, the broader and the simpler the question is, the more likely it is you will get a good answer. It is intended to function as a FAQ database."

	def __init__(self):
		self.message = ""
		self.nick = ""
		self.inittime = ""
		self.connection = connection
	def ircPlug( nick, message, time, channel):
		message = message.lower()
		message = message[len(handeler)+1:]
		messageRay = message.split(" ")
		nick = nick.lower()
		trusted = False
		if nick in trustedNicks:
			trusted = True
			
		#print("______\n%s\n%s\n-------" % (messageRay, message))
		if "hello bot" in message:
			return ("Hello there " + nick + ".")
		elif "remember" in messageRay[0] and "=" in message:
			if trusted:
				findPos = message.find("=")
				startPos = len(messageRay[0])
				qouteDict.update({message[startPos:findPos].strip(" "):message[findPos+1:].strip(" ")})
				#qoutesFile = open("qoutes", "w")
				#qoutesFile.write( "qouteDict=%s\ntrustedNicks=%s" (str(qouteDict), str(trustedNicks))
				#print(qoutesFile.read())
				#qoutesFile.close()
				if saveQoutes() == 1:
					return ("Okay, I'll remember that.")
				else:
					return ("Hmm, seems there might have been an error saving the file... Try again.")
			else:
				return "I don't trust you. >_>"
		elif "reload qoutes" in message:
			if trusted:
				#exec(compile(open("qoutes").read()), "qoutes", 'exec')
				exec(open("qoutes").read())
				return ("Qoutes reloaded.")
			else:
				return ("I don't trust you. >_>")
		elif "add" in messageRay[0]:
			if "trusted" in messageRay[1] and "nick" in messageRay[2]:
				if trusted:
					trustedNicks.append(messageRay[3].lower())
					if saveQoutes() == 1:
						return ("Nick %s added to trusted users." % ( messageRay[3] ) )
					else:
						return "Hmm... There may have been an error saving the file, try again."
				else:
					return "I don't trust you. >_>"
		elif "remove" in messageRay[0]:
			if "trusted" in messageRay[1] and "nick" in messageRay[2]:
				if trusted:
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
					if word in message.lower():
						similarity += 1
					counter+=1
				if counter-similarity < mostSimilar:
					mostSimilar = counter-similarity
					sendQoute = qoute
			if mostSimilar < len(qouteRay)/2:
				sendQoute = qouteDict[sendQoute]
				sendQoute = sendQoute.replace("{nick}", nick)
				return sendQoute
	def shellPlug(args):
		print("QnA shell plugin.")
		exec(open("manage_qoutes.py").read())
