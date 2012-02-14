import random
import os

class Plugin:
	handeler      = "drop:"
	shellHandeler = "drop"
	method        = "args"

	def ircPlug(nick, args, time, channel):
		fileName = "linksdb"
		linksList = []
		filter = [ "boob", "tits", "penis", "sex", "cock", "dick", "fuck", "porn" ]
		if os.path.exists(fileName) == False:
			linksFile = open(fileName, "w")
			linksFile.write("http://www.hackaday.com\n")
			linksFile.close()
		if len(args) == 1:
			linksFile = open(fileName, "r")
			linksList = linksFile.read()
			linksList = linksList.split("\n")
			while "" in linksList:
				linksList.remove("")
			linksFile.close()
			return ("%s" % ( linksList[random.randint(0, len(linksList)-1)]))
		elif len(args) >= 2:
			args = args[1:]
			if args[0] == "remove" and len(args) == 2:
				linksFile = open(fileName, "r")
				linksList = linksFile.read()
				linksList = linksList.split("\n")
				linksFile.close()
				linksFile = open(fileName, "w")
				for link in linksList:
					counter = 0
					if args[1] in link:
						try:
							linksList.remove(link)
						except Exception as e:
							print("Encountered error:" , e)
						print(link)
					counter+=1
				for link in linksList:
					if link != " " and link != "":
						linksFile.write("%s\n" % (link))
				linksFile.close()
			else:
				linksFile = open(fileName, "a")
				for arg in args:
					isClean = True
					for item in filter:
						if item in arg:
							isClean = False
					if "http://" not in arg and "ftp://" not in arg:
						arg = "http://" + arg
					if isClean and arg != " " and arg != "\n":
						linksFile.write("%s\n" % arg)
						return ("%s added to drop database." % arg)
				linksFile.close()
				
	def shellPlug(args):
		print("You gave the args %s." % args)

