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

fp = open("examples/priceIndex.xml", 'r')
productPrice = float(fp.readline().replace('\n', ''))
display("Product price is ", productPrice)
fp.close()
numPurchased = int(input('(Type in value for numPurchased and press Enter): '))
totalPrice = productPrice * numPurchased
display("The total price is ", totalPrice)
