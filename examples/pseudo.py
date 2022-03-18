#from argparse import ArgumentParser
import re

## Parse command line arguments

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", help="increase output verbosity")
args = parser.parse_args()
if args.verbosity:
    print("verbosity turned on")

parser = argparse.ArgumentParser()
parser.add_argument("--src", help="path to pseudocode source file")
parser.add_argument("--dst", help="path to python destination file")
args = parser.parse_args()
print(args)
src = args.src if args.src else "./input.txt"
dst = args.dst if args.dst else "./output.py"

## Pre-processing of input lines

replacements = [
	("\t", ""),
	("“", '"'), # Replace weird quotation marks
	("”", '"'),
	("FALSE", "False"),
	("TRUE", "True"),
	("false", "False"),
	("true", "True"),
	("ELSE IF", "ELIF"),
	("ELSEIF", "ELIF"),
	("ELSIF", "ELIF"),
	("THEN", ""),
	("ROUND", "round"),
	("CONCAT", "concat"),
	("CHARAT", "charat"),
	("SUBSTRING", "substr"),
	("SUBSTR", "substr"),
	("RANDOM", "random"),
	("AND", "and"),
	("OR", "or"),
	("NOT", "not"),
	("(String)", "str"),  # Needs brackets around argument: (String)(argument)
	("(Integer)", "int"), # As above
	("(Double)", "float"), # As above
]

# A crude way to allow array assignment without allocation, e.g. SET x[100] = 42,
# is to secretly make them Python dictionaries!
# Search all lines for such assignments to arrays, and begin the program by
# initialising those variables to empty dictionaries: e.g. x = {}.

arrayVars = set()
r = re.compile(r"SET\s+([^\[=]*)\[")

program = []
print("Pre-processing input lines...")
with open(src, "r") as filePointer:
	for line in filePointer:		
		# Remove trailing comments
		line = re.sub("//.*$", "", line)
		line = re.sub("#.*$", "", line)

		# Remove initial spaces, line number, and trailing spaces
		line = re.sub("^\s*[0-9]*\.?\s*", "", line)

		# Remove final ; or : and any final spaces or newline
		line = re.sub("\s*[;:]\s*$", "", line)

		print("line before:", line)
		# Handle LENGTH
		# Remove gratuitous "[]" and its pre/mid/post whitespace in LENGTH(variable [] )
		line = re.sub("LENGTH\s*\(\s*(\w*)\s*\[\s*\]\s*\)", "LENGTH(\\1)", line) # Don't try to read this...
		line = line.replace("LENGTH", "len")
		print("line after:", line, "\n")

		# If it's an assignment to an array, add to the set of array variable names
		match = r.match(line)
		if match:
			varname = match.group(1).strip()
			if varname not in arrayVars:
				print("Array variable found:", varname)
			arrayVars.add(varname)

		# Finally, go through the list of replacements
		for (old, new) in replacements:
			line = line.replace(old, new)

		print("Input:  ", line)
		# Now add the processed line to the list
		program.append(line)


## Create the output file, line by line

preamble = """### Implementations of pseudocode methods in Python (ignore this part) ###

from random import randrange

def concat(*args):
	result = ""
	for x in args:
		result += str(x)
	return result

def charat(s, i):
	return s[i]

def substr(s, a, b):
	return s[a:b]

def random(a, b):
	return randrange(a, b + 1)
"""

# Start with the preamble (built-in methods)...
outputLines = [preamble]

# Initialise the fake arrays which are actually dictionaries (see comment above)
if arrayVars != set():
	outputLines.append('# Initialise "arrays" (actually dictionaries, to simplify allocation)\n')
	for var in arrayVars:
		outputLines.append(var + " = {}")

outputLines.append("### Your converted code starts here ###\n")

# We don't know if an OPENed file will be used for reading or writing.
# But we need to know before we can open the file in Python.
# We'll record filePath when it is OPENed, but only open it
# when we see READ or WRITE (fileMode is "r" or "w" respectively)
# and assume that we do not combine READs and WRITEs to an open file.
# We assume there is no complicated control flow: every OPEN statement
# in the pseudocode is matched by the following CLOSE statement.

filePath = None
fileOpen = False

whileLevel = 0
ifLevel = 0
lineNum = 0

for line in program:
	lineNum += 1
	indentLevel = (whileLevel + ifLevel) # Will be unindented on ELSE and ELIF lines
	
	# Create a single output line, or a list of lines (see READ/WRITE) from this line
	if line.startswith("DECLARE") or line.startswith("#") or line.startswith("PROGRAM") or line.strip() == "END" or line.startswith("START") or line.startswith("BEGIN"):
		output = f"# Ignored: {line}"
	elif line == "" or line.isspace(): # Empty line
		output = ""
	elif line.startswith("DISPLAY"):
		# Replace DISPLAY with print, and attempt to replace + with ,
		# e.g. DISPLAY "aaa" + x + "bbb" + y ----> print("aaa", x, "bbb", y)
		line = re.sub("DISPLAY ?", "print(", line).strip() + ")"
		line = re.sub('("[^"]*?")\s*\+\s*', '\\1, ', line)
		output = re.sub('\s*\+\s*("[^"]*?")', ', \\1', line)
	elif line.startswith("GET"):
		variable = line.replace("GET", "").strip()
		output = f"{variable} = input('(Type in value for {variable} and press Enter): ')"
	elif line.startswith("SET"):
		output = line.replace("SET", "").strip()
	elif line.startswith("OPEN"):
		if filePath != None:
			print(f"Error on line {lineNum}: Trying to OPEN a file but it appears a previous OPEN file {filePath} was not CLOSEd.")
			exit(1)
		filePath = line.replace("OPEN", "").strip()
		output = ""
	elif line.startswith("CLOSE"):
		if filePath == None:
			print(f"Error on line {lineNum}: Trying to CLOSE a file but it appears no file was OPENed.")
			exit(1)
		filePath = None
		fileOpen = False
		output = "fp.close()"
	elif line.startswith("READ"):
		if filePath == None:
			print("Error on line {lineNum}: Trying to READ data but it seems no file is OPEN")
			exit(1)
		if not fileOpen:
			output = [f"fp = open({filePath}, 'r')"]
			fileOpen = True
		else:
			output = []
		variable = line.replace("READ", "").strip()
		output.append(f"{variable} = fp.readline().replace('\\n', '')")
	elif line.startswith("WRITE"):
		if filePath == None:
			print("Error on line {lineNum}: Trying to WRITE data but it seems no file is OPEN")
			exit(1)
		if not fileOpen:
			output = [f"fp = open({filePath}, 'w')"]
			fileOpen = True
		else:
			output = []
		expression = line.replace("WRITE", "").strip()
		output.append(f"fp.writeline({expression})")
	elif line.startswith("WHILE"):
		whileLevel += 1
		output = line.replace("WHILE", "while").strip() + ":"
	elif line.startswith("IF"):
		ifLevel += 1
		output = line.replace("IF", "if").strip() + ":" # Extra space in case of trailing brackets
	elif line.startswith("ELSE"):
		output = "else:"
		indentLevel -= 1
	elif line.startswith("ELIF"):
		output = line.replace("ELIF", "elif")
		indentLevel -= 1
	elif line.startswith("ENDIF"):
		output = ""
		ifLevel -= 1
	elif line.startswith("ENDWHILE"):
		output = ""
		whileLevel -= 1
	else:
		print(f"Didn't understand line {lineNum}: {line}")
		exit(1)

	indent = indentLevel * "    "
	# Output can be a single line, or a list of lines. Either way, make it into a list.
	if not isinstance(output, list):
		output = [output]

	for outputLine in output:
		if outputLine != "":
			outputLines.append(indent + outputLine)


## Write the resulting lines to the destination path

with open(dst, "w") as filePointer:
	for outputLine in outputLines:
		print("Output: ", outputLine)
		filePointer.write(outputLine + "\n")








