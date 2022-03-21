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

email = str(input('(Type in value for email and press Enter): '))
found = False
index = 0
runLoop = (found == False and index < len(email))
display("Email is: ", email)
display("About to enter loop")
while runLoop:
    display("index is ", index)
    display("--Character at this index: ", charat(email, index))
    if charat(email, index) == "@":
        display("----Found the @ symbol")
        found = True
    else:
        display("----It is not the @ symbol")
    index = index + 1
    runLoop = (found == False and index < len(email))
    display("--Value of runLoop: ", runLoop)
if found == True:
    display("Email contains @")
else:
    display("Email does not contain @")
