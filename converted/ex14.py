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

stringInput = str(input('(Type in value for stringInput and press Enter): '))
currentIndex = 0
xCount = 0
while currentIndex < len(stringInput):
    currentChar = charat(stringInput, currentIndex)
    display(currentChar)
    if currentChar == "X":
        xCount = xCount + 1
    currentIndex = currentIndex + 1
display("Your string contains ", xCount, " Xs")
