#!/bin/python3
# This is shell of sorts to edit the qoutes file quickly and easily without messing it up.
print("Qoute manager shell v0.1 for raspircBot\n")
exec(compile(open("qoutes").read(), "qoutes", 'exec'))

commandHash = [ "list", "remove", "add", "exit", "help" ]
def managerHelp():
	print("""Commands:		
	list
	remove number
	add qoute = answer
	qoute number
	nicks
	newnick nick
	delnick number
	help
	exit
	
	Note: You must use the exit command to save changes to qoutes.""")

userInput = ""
counter = 0
running = True
while running:
	userInput = input("> ")
	qouteList = list(qouteDict.keys())
	if userInput[:4] == "list":
		counter = 0
		for qoute in qouteList:
			print("%3s | %s" % (str(counter), qoute))
			counter += 1
	elif userInput[:5] == "nicks":
		counter = 0 
		for nick in trustedNicks:
			print("%3s | %s" % (str(counter), nick))
			counter+=1
	elif userInput[:6] == "remove" and len(userInput) > 6:
		try:
			qouteDict.pop(qouteList[int(userInput[7:])])
		except Exception:
			print("Dat doesn't exist n00b.")
	elif userInput[:3] == "add" and "=" in userInput:
		findPos = userInput.find("=")
		qouteDict.update({userInput[4:findPos].strip(" "):userInput[findPos+1:].strip(" ")})
	elif userInput[:5] == "qoute" and len(userInput) > 5:
		try:
			print( qouteDict[ qouteList[ int(userInput[6:]) ]] )
		except Exception:
			print("Dat doesn't exist n00b.")
	elif userInput[:7] == "newnick" and len(userInput) > 7:
		trustedNicks.append(userInput[8:])
	elif userInput[:7] == "delnick" and len(userInput) > 7:
		try:
			trustedNicks.pop(int(userInput[8:]))
		except Exception:
			print("Dat doesn't exist n00b.")
	elif userInput == "help":
		managerHelp()
	elif userInput == "exit":
		print("Do you want to save the changes?")
		userInput = input("Y/N > ")
		if userInput.lower() == "y" or userInput.lower() == "yes":
			qoutesFile=open("qoutes", "w")
			qoutesFile.write("qouteDict= "+ str(qouteDict) +"\ntrustedNicks=" + str(trustedNicks))
			qoutesFile.close()
			print("file saved.")
			running = False
		else:
			print("File not saved.")
			running = False
	else:
		print("Unknown command.")
	
			
