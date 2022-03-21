### Implementations of pseudocode methods in Python (ignore this part) ###

from random import randrange

def display(*args):
	print(*args, sep="")

def concat(*args):
	result = ""
	for x in args:
		result += str(x)
	return result

def charat(s, i):
	return s[i]

def substr(s, a, b):
	return s[a:(b+1)]

def random(a, b):
	return randrange(a, b + 1)

print(f"[1m(Remember to re-run 'pseudo.py' if you edit the source pseudocode!)[0m")

### Your converted code starts here ###

tankCapacity = 100
reserveLevel = 10
currentLevel = float(input('(Type in value for currentLevel and press Enter): '))
percentRemaining = (currentLevel / tankCapacity) * 100
display("Current Fuel Level is ", round(percentRemaining, 0), " percent")
if percentRemaining < 10:
    display("Warning. Reserve Fuel Level")
