import sys
from lexer import lexer
from parser import runFromTerminal, runFromFile

class VariableExistsError(Exception):
    pass

class ReDeclarationError(Exception):
    pass

variables = {}


def run(p, variables_list):
    #global variables
    if(type(p) == tuple):
    # Expressions
        if(p[0] == "first"):
            return run(p[1], variables_list)
        if(p[0] == "negative"):
            return -1*run(p[1], variables_list)
        if(p[0] == "list"):
            return run(p[1], variables_list)
        
        if(p[0] == "*"):
            return run(p[1], variables_list) * run(p[2], variables_list)
        elif(p[0] == "/"):
            val1 = run(p[1], variables_list)
            val2 = run(p[2], variables_list)
            if val2 == 0:
                raise ZeroDivisionError(lexer.lineno)
            return val1 / val2
        elif(p[0] == "+"):
            return run(p[1], variables_list) + run(p[2], variables_list)
        elif(p[0] == "-"):
            return run(p[1], variables_list) - run(p[2], variables_list)
        elif(p[0] == "^"):
            return run(p[1], variables_list) ** run(p[2], variables_list)
        elif(p[0] == "%"):
            return run(p[1], variables_list) % run(p[2], variables_list)
        elif(p[0] == "<"):
            return run(p[1], variables_list) < run(p[2], variables_list)
        elif(p[0] == ">"):
            return run(p[1], variables_list) > run(p[2], variables_list)
        elif(p[0] == "<="):
            return run(p[1], variables_list) <= run(p[2], variables_list)
        elif(p[0] == ">="):
            return run(p[1], variables_list) >= run(p[2], variables_list)
        elif(p[0] == "and"):
            return run(p[1], variables_list) and run(p[2], variables_list)
        elif(p[0] == "or"):
            return run(p[1], variables_list) or run(p[2], variables_list)
        elif(p[0] == "!="):
            return run(p[1], variables_list) != run(p[2], variables_list)
        elif(p[0] == "=="):
            return run(p[1], variables_list) == run(p[2], variables_list)
        
        elif(p[0] == "not"):
            return not run(p[1], variables_list)
        
        elif(p[0] == "++"):
            if(type(p[1]) == tuple and p[1][0] == "var"):
                return run(('mutate', p[1][1], ('+', run(p[1], variables_list), 1)), variables_list)
            return run(p[1], variables_list) + 1
        elif(p[0] == "--"):
            if(type(p[1]) == tuple and p[1][0] == "var"):
                return run(('mutate', p[1][1], ('+', run(p[1], variables_list), -1)), variables_list)
            return run(p[1], variables_list) - 1

        # Variables
        elif(p[0] == "assign"):
            if p[2] in variables_list[0]:
                raise ReDeclarationError(p[2])
                #print(p[2] + " variable phele bana howa hai")
                #raise VariableExistsError(p[2], lexer.lineno)
            val = run(p[3], variables_list)
            if(type(val) == p[1]):
                variables_list[0][p[2]] = val
                return val
            #print(type(val), ": type ke value ke type ", p[1]," nahi ho sakte")
            raise TypeError("assign", type(val), p[1])
        elif(p[0] == "mutate"):
            val = run(p[2], variables_list)
            for variables in variables_list:
                if p[1] in variables:
                    if(type(val) == type(variables[p[1]])):
                        variables[p[1]] = val
                        return val
                    raise TypeError("mutate", p[1], type(val), type(variables[p[1]]))
                    #print(p[1] + " ke type ", type(val), " variable ke type ", type(variables[p[1]]), " se match nahi ker rahi")
                    #return

            raise NameError(p[1])
            #print(p[1] +" ko declare nahi kia gaya")
            #return
        elif(p[0] == "var"):
            for variables in variables_list:
                if p[1] in variables:
                    return variables[p[1]]

            raise NameError(p[1])
            #print("Ye variable wajood mai nahi hai: " + p[0])
            #return 

        # List
        elif(p[0] == "list_funcs"):
            args = list(map(lambda x: run(x, variables_list), p[3]))
            val =  run(p[2], variables_list)
            if(p[1] == "pop"):
                return val.pop(*args)
            if(p[1] == "push"):
                return val.append(*args)
            if(p[1] == "index"):
                return val[args[0]]
            if(p[1] == "slice"):
                return val[args[0]:args[1]]
        

        # Do While
        elif(p[0] == "while"):
            variables_list.insert(0, {})
            run(p[1], variables_list)
            break_handler = True
            for line in p[1]:
                if line == "toro":
                    break_handler = False
                    break
                elif line ==  "jariRakho":
                    break
                run(line, variables_list)
            while(run(p[2], variables_list) and break_handler):
                for line in p[1]:
                    if line == "toro":
                        break_handler = False
                        break
                    elif line ==  "jariRakho":
                        break
                    run(line, variables_list)
            
            variables_list = variables_list[1:]
            return

        # Printing 
        elif(p[0] == "print"):
            to_print = list(map(lambda x: run(x, variables_list), p[1]))
            print(*to_print)
    else:
        return p

def main():
    if(len(sys.argv) == 1):
        while(True):
            try:
                parser = runFromTerminal()
                if(parser == None):
                    break
                for line in parser:
                    print(run(line, [variables]))
            except ReDeclarationError as e:
                print("ReDeclarationError: " ,"Line", lexer.lineno , ", Variable phele se bana howa hai: ", e.args[0])
            except TypeError as e:
                if(e.args[0] == 'assign'):
                    print("TypeError: " ,"Line:",lexer.lineno, ", ", e.args[1], ": type ke value ke type ", e.args[2]," nahi ho sakte")
                elif(e.args[0] == 'mutate'):
                    print("TypeError: " ,"Line:",lexer.lineno ,", Variable: ",e.args[1] + " ke type ", e.args[2], ", variable ke type ", e.args[3], ", se match nahi ker rahi")
                else:
                    print("TypeError: " ,"Line:", lexer.lineno, ", ", e)
            except NameError as e:
                print("NameError: ", "Line: ", lexer.lineno, ", ", "Variable \"", e.args[0] ,"\" ko declare nahi kia gaya")
            except SyntaxError as e:
                if(e.args[0] == "lexer"):
                    print("SyntaxError: ", "Line: " , e.args[1],"Ghair Kanooni lafz: '%s'" %e.args[2])
                elif(e.args[0] == "parser"):
                    print("SyntaxError: Line,", e.args[1], ", Is lafz ke tawaqo nahi the: " , e.args[2])
                else:
                    print(e.args[0])
            except Exception as e:
                print("Error: ", "Line: ", lexer.lineno, ", ", e)

    else:
        try:
            parser = runFromFile(sys.argv[1])
            if(parser == None):
                return -1
            else:
                for line in parser:
                    run(line, [variables])
        except ReDeclarationError as e:
            print("ReDeclarationError: ", " Variable phele se bana howa hai: ", e.args[0])
        except TypeError as e:
            if(e.args[0] == 'assign'):
                print("TypeError: " , e.args[1], ": type ke value ke type ", e.args[2]," nahi ho sakte")
            elif(e.args[0] == 'mutate'):
                print("TypeError: ", "Variable: ",e.args[1] + " ke type ", e.args[2], ", variable ke type ", e.args[3], ", se match nahi ker rahi")
            else:
                print("TypeError: " , e)
        except NameError as e:
            print("NameError: ", "Line: ", lexer.lineno, ", ", "Variable \"", e.args[0] ,"\" ko declare nahi kia gaya")
        except SyntaxError as e:
            if(e.args[0] == "lexer"):
                print("SyntaxError: ", "Line: " , e.args[1],"Ghair Kanooni lafz: '%s'" %e.args[2])
            elif(e.args[0] == "parser"):
                print("SyntaxError: Line,", e.args[1], ", Is lafz ke tawaqo nahi the: " , e.args[2])
            else:
                print(e.args[0])
        except Exception as e:
            print("Error: ", e)


if __name__ == "__main__":
    main()
