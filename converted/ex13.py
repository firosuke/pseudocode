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

letters = {}

### Your converted code starts here ###

letters[0] = "A"
letters[1] = "B"
letters[2] = "C"
letters[3] = "D"
letters[4] = "E"
i = 0
concatString = ""
while i < len(letters):
    concatString = concat(concatString, letters[i])
    i = i + 1
display("Concatenated string: ", concatString)
display("There are ", i, " letters total")
