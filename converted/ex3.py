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

examScores = {}

### Your converted code starts here ###

examScores [0] = 22
examScores [1] = 44
examScores [2] = 67
examScores [3] = 45
examScores [4] = 74
counter = 0
totalScore = 0
while counter < len(examScores):
    display("Read score: ", examScores[counter])
    totalScore = totalScore + examScores [counter]
    counter = counter + 1
averageScore = totalScore / len(examScores)
display("Average of scores is: ", averageScore)
