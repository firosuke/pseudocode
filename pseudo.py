from argparse import ArgumentParser
import re
from sys import exit

####################### Constants #######################

# Some colors for warnings
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Map of lowercase pseudocode type names, to their python equivalents
typeMap = {
	"integer":"int", 
	"double":"float", 
	"float":"float",
	"boolean":"bool",
	"character":"str",
	"string":"str"
	}


# List of simple translations from pseudocode to python
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
	("(Character)", "str"), # As above
]


# Some regular expressions

reFlags = re.VERBOSE # Allows whitespace in regexes. Also can add: "| re.IGNORECASE"

rSetArray = re.compile(r"SET \s+ (\w+) \s* \[", reFlags) # regex for SET array command

# regex for first part of DECLARE commands: everything up to the first comma
reFirst = re.compile("""
		DECLARE                             # Start of DECLARE statement
	\s+	(?: CONSTANT | CONST | Constant)?   # (We ignore constants)
	\s* ( \w+ )                             # Type
	\s+ ( \w+ )(?: \s* \[ \s* \] )?         # Variable name, possibly with [] if array
	\s* """, reFlags)

# regex for each (comma-separated) remaining part of a DECLARE command
# (same as "variable name" in reFirst above)
reRest = re.compile(""" \s* ( \w+ )(?: \s* \[ \s* \] )? \s* """, reFlags)


# Preamble for generated python file

preamble = """### Implementations of pseudocode methods in Python (ignore this part) ###

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

"""

preamble += f'print(f"{bcolors.BOLD}(Remember to re-run \'pseudo.py\' if you edit the source pseudocode!){bcolors.ENDC}")\n'



####################### Parse command line arguments #######################

print("Parsing command-line arguments...")

parser = ArgumentParser()
parser.add_argument("src", nargs="?", help="path to pseudocode source file")
parser.add_argument("dst", nargs="?", help="path to python destination file")
args = parser.parse_args()

if not args.src:
	print(f"No source given, going to try and read from file: {bcolors.UNDERLINE}input.txt{bcolors.ENDC}")
	src = "input.txt"
else:
	print(f"Going to try and read from file: {bcolors.UNDERLINE}{args.src}{bcolors.ENDC}")
	src = args.src

if not args.dst:
	print(f"No destination given, going to try and write to file: {bcolors.UNDERLINE}output.py{bcolors.ENDC}")
	dst = "output.py"
else:
	print(f"Going to try and write to file: {bcolors.UNDERLINE}{args.dst}{bcolors.ENDC}")
	dst = args.dst


####################### Pre-processing of input lines #######################

print(f"Reading and processing input from {bcolors.UNDERLINE}{src}{bcolors.ENDC}...")

# A crude way to allow array assignment without allocation, e.g. SET x[100] = 42,
# is to secretly make them Python dictionaries!
# Search all lines for such assignments to arrays, and begin the program by
# initialising those variables to empty dictionaries: e.g. x = {}.

varTypes = {}
arrayVars = set()

program = []
lineNum = 0
with open(src, "r") as filePointer:
	for line in filePointer:
		lineNum += 1
		# Remove trailing comments
		line = re.sub("//.*$", "", line)
		line = re.sub("#.*$", "", line)

		# Remove initial spaces, line number, and trailing spaces
		line = re.sub("^\s*\d*[.:]?\s*", "", line)

		# Remove final ; or : and any final spaces or newline
		line = re.sub("\s*[;:]\s*$", "", line)

		# Handle LENGTH
		# Remove gratuitous "[]" and its pre/mid/post whitespace in LENGTH(variable [] )
		line = re.sub("LENGTH\s*\(\s*(\w*)\s*\[\s*\]\s*\)", "LENGTH(\\1)", line)
		line = line.replace("LENGTH", "len")

		# If it's a variable declaration, record those types for the variables
		# (Arrays treated the same as non-arrays) This is used when GETting into
		# the variables, so that the incoming string can be converted to the
		# appropriate type
		if line.startswith("DECLARE"):
			firstPart, *rest = line.split(sep=",")
			varType, firstVarName = reFirst.match(firstPart).groups()
			otherVarNames = list(map(lambda x: reRest.match(x).groups()[0], rest))

			for varName in [firstVarName] + otherVarNames:
				if varType.lower() not in typeMap.keys():
					print(f"Line {lineNum}: Did not recognise variable type {varType}")
					print("Expected (some capitalisation of): " + ", ".join(list(typeMap.keys())))
					exit(1)
				varTypes[varName] = typeMap[varType.lower()]

		# If it's an assignment to an array, add to the set of array variable names
		match = rSetArray.match(line)
		if match:
			varname = match.group(1).strip()
			#if varname not in arrayVars:
			#	print("Array variable found:", varname)
			arrayVars.add(varname)

		# Finally, go through the list of replacements
		for (old, new) in replacements:
			line = line.replace(old, new)

		#print("Input:  ", line)

		# Now add the processed line to the list
		program.append(line)


####################### Create output file #######################

print("Creating output file...")

# Start with the preamble (built-in methods, etc)...
outputLines = [preamble]

# Initialise the fake arrays which are actually dictionaries (see comment above)
if arrayVars != set():
	outputLines.append('\n# Initialise "arrays" (actually dictionaries, to simplify allocation)\n')
	for var in arrayVars:
		outputLines.append(var + " = {}")
	outputLines.append('')

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
		output = ""
	elif line == "" or line.isspace(): # Empty line
		output = ""
	elif line.startswith("DISPLAY"):
		# Replace DISPLAY with display() method (see preamble), and replace + with ,
		# e.g. DISPLAY "aaa" + x + "bbb" + y ----> display("aaa", x, "bbb", y)
		line = re.sub("DISPLAY ?", "display(", line).strip() + ")"
		line = re.sub('("[^"]*?")\s*\+\s*', '\\1, ', line)
		output = re.sub('\s*\+\s*("[^"]*?")', ', \\1', line)
	elif line.startswith("GET"):
		variable = line.replace("GET", "").strip()
		if variable not in varTypes:
			print(f'{bcolors.WARNING}Warning: Line {lineNum}: GETting user input to variable "{variable}" with no declared type (assuming String){bcolors.ENDC}')
			varTypes[variable] = "str"
		output = f"{variable} = {varTypes[variable]}(input('(Type in value for {variable} and press Enter): '))"
	elif line.startswith("SET"):
		output = line.replace("SET", "").strip()
	elif line.startswith("OPEN"):
		if filePath != None:
			print(f"{bcolors.FAIL}Error on line {lineNum}: Trying to OPEN a file but it appears a previous OPEN file {filePath} was not CLOSEd.{bcolors.ENDC}")
			exit(1)
		filePath = line.replace("OPEN", "").strip()
		output = ""
	elif line.startswith("CLOSE"):
		if filePath == None:
			print(f"{bcolors.FAIL}Error on line {lineNum}: Trying to CLOSE a file but it appears no file was OPENed.{bcolors.ENDC}")
			exit(1)
		filePath = None
		fileOpen = False
		output = "fp.close()"
	elif line.startswith("READ"):
		if filePath == None:
			print(f"{bcolors.FAIL}Error on line {lineNum}: Trying to READ data but it seems no file is OPEN.{bcolors.ENDC}")
			exit(1)
		if not fileOpen:
			output = [f"fp = open({filePath}, 'r')"]
			fileOpen = True
		else:
			output = []
		variable = line.replace("READ", "").strip()
		if variable not in varTypes:
			print(f'{bcolors.WARNING}Warning: Line {lineNum}: Reading from file into variable "{variable}" with no declared type (assuming String){bcolors.ENDC}')
			varTypes[variable] = "str"
		output.append(f"{variable} = {varTypes[variable]}(fp.readline().replace('\\n', ''))")
	elif line.startswith("WRITE"):
		if filePath == None:
			print(f"{bcolors.FAIL}Error on line {lineNum}: Trying to WRITE data but it seems no file is OPEN.{bcolors.ENDC}")
			exit(1)
		if not fileOpen:
			output = [f"fp = open({filePath}, 'w')"]
			fileOpen = True
		else:
			output = []
		expression = line.replace("WRITE", "").strip()
		output.append(f"fp.write(str({expression}) + '\n')")
	elif line.startswith("WHILE"):
		whileLevel += 1
		output = line.replace("WHILE", "while").strip() + ":"
	elif line.startswith("IF"):
		ifLevel += 1
		output = line.replace("IF", "if").strip() + ":" # Extra space in case of trailing brackets
	elif line.startswith("ELSE"):
		if ifLevel == 0:
			print(f"{bcolors.FAIL}Error on line {lineNum}: ELSE with no preceding IF.{bcolors.ENDC}")
			exit(1)
		output = "else:"
		indentLevel -= 1
	elif line.startswith("ELIF"):
		if ifLevel == 0:
			print(f"{bcolors.FAIL}Error on line {lineNum}: ELSEIF with no preceding IF.{bcolors.ENDC}")
			exit(1)
		output = line.replace("ELIF", "elif").strip() + ":"
		indentLevel -= 1
	elif line.startswith("ENDIF"):
		if ifLevel == 0:
			print(f"{bcolors.FAIL}Error on line {lineNum}: ENDIF with no preceding IF.{bcolors.ENDC}")
			exit(1)
		ifLevel -= 1
		output = ""
	elif line.startswith("ENDWHILE"):
		if whileLevel == 0:
			print(f"{bcolors.FAIL}Error on line {lineNum}: ENDWHILE with no preceding WHILE.{bcolors.ENDC}")
			exit(1)
		output = ""
		whileLevel -= 1
	else:
		print(f'{bcolors.FAIL}Error: line {lineNum}: Couldn\'t understand line: "{line.strip()}"{bcolors.ENDC}')
		exit(1)

	indent = indentLevel * "    "
	# Output can be a single line, or a list of lines. Either way, make it into a list.
	if not isinstance(output, list):
		output = [output]

	for outputLine in output:
		if outputLine != "":
			outputLines.append(indent + outputLine)

# If we end the program inside an IF or WHILE, that's an error
if ifLevel > 0 or whileLevel > 0:
	print(f"{bcolors.FAIL}Error: Program is missing an ENDIF or ENDWHILE.{bcolors.ENDC}")
	exit(1)

if filePath != None:
	print(f"{bcolors.FAIL}Error: Program did not CLOSE the open file: {filePath}.{bcolors.ENDC}")
	exit(1)


####################### Write output to destination path #######################

print(f"Writing output file to {bcolors.UNDERLINE}{dst}{bcolors.ENDC}...")

with open(dst, "w") as filePointer:
	for outputLine in outputLines:
		#print("Output: ", outputLine)
		filePointer.write(outputLine + "\n")

print(f'Done. You can now run: {bcolors.BOLD}python {dst}{bcolors.ENDC} ')