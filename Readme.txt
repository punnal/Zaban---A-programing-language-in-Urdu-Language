##############################################################################
About:
Language name: Zaban
Description: This is a programming language written in Urdu language.
Creater: Punnal Ismail Khan
##############################################################################


##############################################################################
Running a test case or any file written in zaban:
run: python3 interpreter.py filename.txt
##############################################################################


##############################################################################
Accessing Zaban Shell in terminal:
run: python3 interpreter.py
##############################################################################


##############################################################################
Synatx:
Look at the testcases files. it covers the whole syntax except few statements.
Below is the list of syntax suppoted but is not present in test cases:
	a. break statement: which is represented by word 'toro' in zaban
	b. continue statement: which is represented by word 'jariRakho' in zaban

##############################################################################


##############################################################################
Features Implemented:
Variables:
	a. Declaration, assignment, access
	b. Static-typing (types restricted to: int, double, char, string, bool)
	c. Initialisation and declaration of a variable with the name of a pre existing variable should generate an error.
Expressions:
	a. Numerical Operators: (+ , - , / , * , ^, % , ++, --)
	b. Logical Operators (<, >, <=,>=, !=, ==, NOT, AND, OR)
	c. Nested parentheses
	d. Type (e.g. for String + Int) and division by 0 errors
Standard Output:
	a. Single object is printed with a line break.
	b. Multiple objects separated by a delimiter (e.g. comma as in Python) are printed withspaces in between and a line break at the end.
Do-While Loops:
	a. Can be nested
List:
	a. Declaration, assignment, access
	b. Access outside the list-size should also give an error (e.g. Index Out of Bounds)
	c. list.pop(index of item to remove) // list.pop(0) removes the head of the list and returns it
	d. list.push(value) // appends the value at the end of the list
	e. list.index(index) // returns the value at that index