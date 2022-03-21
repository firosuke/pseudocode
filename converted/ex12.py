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

interest = 1.15
fp = open("examples/interest.xml", 'r')
amount = float(fp.readline().replace('\n', ''))
duration = int(fp.readline().replace('\n', ''))
fp.close()
interest = (amount * interest * duration)
display("Simple interest on ", amount, " for ", duration, " years is: ", interest)
