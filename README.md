# pseudocode

This is a script to convert pseudocode (as taught at Birkbeck College London) into a python script, which you can then run to see your pseudocode in action.

It is not complete, but it should work for "simple" pseudocode.
There is a limited set of pseudocode commands it can recognise. These are described below in the section "Supported Pseudocode". If you don't type these as specified, it may fail.

If there are errors in the pseudocode, the conversion will fail with some Python errors. 
The displayed error might give you a clue about the problem. If not, try to contact me.

## How to use

You can download the files from this repo as a ZIP file. (If you are viewing this in GitHub, click on the "Code" button above-right, and then click "Download as ZIP".) You should be able to open the ZIP file on your computer and/or extract it to a convenient location.
(Or if you have git installed on your computer, from the command prompt / shell, run: git clone https://github.com/firosuke/pseudocode/)

If all else fails, just click on pseudo.py file and copy-paste the code, save it onto your computer.
The only essential file is the Python script, pseudo.py. (There are some example pseudocode files and example data in the examples folder.)

Run the script like this, from your terminal (Linux/Mac) or command prompt (Windows) after navigating to the folder where you have placed pseudo.py:

python pseudo.py (path to your source file) (destination file)

For example:
python pseudo.py examples/ex12.txt simple-interest.py

If you leave out the source file, it will look for "input.txt" in the current folder. 
If you leave out the destination file, it will write the generated python code into "output.py".

It will display some information about what it is doing while it runs.
If successful, you can try to run the generated python script. For example:

python simple-interest.py

If the conversion went well, you will see your pseudocode in action.
Note that if there are something wrong, Python will get confused and you will see Python errors. As mentioned above, this may happen if you don't type the pseudocode in a particular way that this script recognises: see "Supported Pseudocode" below. If you think you've done it correctly, there may be a problem or unmentioned limitation of this script -- let me know.

## Supported Pseudocode

- DECLARE (CONSTANT/CONST) <type> <variable> (can be followed by: , <variable>, <variable>, ...)
- DISPLAY "this string" + some expression + "that string", etc. (Essentially reduced to "print" in python.)
- IF condition, ELSE IF, ELSE, ENDIF
- WHILE condition, ENDWHILE
- SET variable = expression
- GET variable
- OPEN "your-file-path" (see note below)
- READ variable
- WRITE variable
- CLOSE "your-file-path"
- Boolean operators AND, OR, NOT; and values True or False
- ROUND(number, decimalPlaces)
- CONCAT(string1, string2, ...)
- RANDOM(upper, lower)
- CHARAT(string, index)
- SUBSTRING(string, start, end) (including the end index)
- Type conversions: (String), (Integer), (Double), (Boolean), followed by an expression which must be in brackets. E.g.: (Integer)(stockPrice)

Notes:
  
Variable names are allowed to contain upper- and lower-case letters, and numbers, and underscore. Nothing else -- in particular, no spaces.
Strings are expected to appear in double quotes "" (or the fancier quotes “”). You might get away with single quotes.

The datatypes mentioned in the course are: Boolean, String, Double (i.e. "float" or decimal), Integer, Char.
(These are translated into python as: bool, str, float, float, int, str.)

For simplicity, line numbers, end-of-line semicolons, spacing, and CONSTANT declarations are ignored or removed.
That doesn't mean you should leave them out of your pseudocode :-)

Keywords like GET and READ are expected to be in capitals as shown below.
Types and values like Boolean, String, True, False... are expected to have this capitalisation.

You can GET or READ into one cell of an array. For example: "GET scores[0]". Or, "READ name[i]".

If you GET user input into a variable, or READ a file into a variable, that variable should have a declared type. The generated script will try to get one line of input from a file (READ) or the user (GET), and convert it to that type. If no type is declared, the script will display a warning that we are assuming it is a string (which may not be what you want).

After you OPEN a file, you can either READ or WRITE, but not both. When you no longer need it, you should CLOSE the file. (You can OPEN it again if you need to either READ or WRITE again.) For simplicity, you can only open one file at a time, and each OPEN should be followed by a matching CLOSE, simply the next one in the file.
(*Aside: In Python you have to decide when you open a file, whether you want to read or write from it. But in pseudocode, we ignore this detail. So the conversion has to do some extra work to allow it.*)

You can put values into an array simply by assigning them directly: e.g. SET names[25] = "Adam". 
(*Aside: Most programming languages don't let you do this. You have to initialise the array. But we can get around this detail by secretly using Python dictionaries to represent arrays, because if a dictionary doesn't yet have a key (e.g. 25 above), when we do the assignment, it will simply create the new key.*)

