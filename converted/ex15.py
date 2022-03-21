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


# Initialise "arrays" (actually dictionaries, to simplify allocation)

integers = {}

### Your converted code starts here ###

display("Starting program")
integers[0] = 98
integers[1] = 55
integers[2] = 98
integers[3] = 32
integers[4] = 100
integers[5] = 0
highest = integers[0]
index = 1
display("Index is:", index)
display("Highest is:", highest)
display("Starting the loop")
while index < len(integers):
    display("Just entered the loop, index is:", index)
    display("-- The next integer is:", integers[index])
    if integers[index] > highest:
        display("-- New highest number")
        highest = integers[index]
    elif integers[index] == highest:
        display("-- This is the same as the highest so far")
    else:
        display("-- This is smaller than the highest so far")
    display("-- highest is now:", highest)
    index = index + 1
display("Loop finished")
display("Highest is:", highest)
