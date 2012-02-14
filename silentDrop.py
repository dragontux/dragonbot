import random
import os

class Plugin:
	handeler      = ""
	shellHandeler = "sDrop"
	method        = "args"

	def ircPlug(nick, args, time, channel):
		fileName = "linksdb"
		linksList = []
		filter = [ "boob", "tits", "penis", "cock", "dick", "fuck", "porn" ]
		if os.path.exists(fileName) == False:
			linksFile = open(fileName, "w")
			linksFile.write("http://www.hackaday.com\n")
			linksFile.close()
		if len(args) >= 1:
			linksFile = open(fileName, "a")
			for arg in args:
				isClean = True
				for item in filter:
					if item in arg:
						isClean = False
				if "http://"  in arg or "https://" in arg or "ftp://" in arg:
					if isClean:
						linksFile.write("%s\n" % arg)
			linksFile.close()
				
	def shellPlug(args):
		print("You gave the args %s." % args)
