colorDict = { 
	"black"  :'\033[0;30m',
	"red"    :'\033[0;31m',
	"green"  :'\033[0;32m',
	"yellow" : '\033[0;33m',
	"blue"   : '\033[0;34m',
	"purple" : '\033[0;35m',
	"cyan"   : '\033[0;36m',
	"white"  : '\033[0;37m',
	
	"boldblack"  : '\033[1;30m',
	"boldred"    : '\033[1;31m',
	"boldgreen"  : '\033[1;32m',
	"boldyellow" : '\033[1;33m',
	"boldblue"   : '\033[1;34m',
	"boldpurple" : '\033[1;35m',
	"boldcyan"   : '\033[1;36m',
	"boldwhite"  : '\033[1;37m',

	"endchar"    : '\033[0m'
}

def printColor(text, color):
	if color in colorDict:
		print( colorDict[color] + text + colorDict["endchar"] )
	else:
		print("Color " + color + " not found!")
