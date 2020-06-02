import sys
import ply.yacc as yacc
from lexer import tokens

start = "lines"

precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQUALEQUAL'),
        ('left', 'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE'),
        ('left', 'POWER'),
        ('right', 'NOT'),
)
# Error

def p_error(p):
    if p == None:
        raise SyntaxError("SyntaxError: Expected further input")
    else:
        raise SyntaxError("parser", p.lineno, p.value)

# Basic layout of language

def p_lines(p):
    '''
    lines : line END lines
    '''
    p[0] = [p[1]] + p[3]

def p_lines_last(p):
    '''
    lines : line
    '''
    p[0] = [p[1]]

def p_lines_no(p):
    '''
    lines :
    '''
    p[0] = []

def p_while(p):
    '''
    while : DO CLPARN lines CRPARN WHILE LPARN expression RPARN
    '''
    p[0] = ("while", p[3], p[7])

def p_while_statements(p):
    '''
    statement : BREAK
             | CONTINUE
    '''
    p[0] = p[1]

def p_line(p):
    '''
    line : print
         | while
         | expression
         | variable_assign
         | statement
         | empty
    '''
    #print(run(p[1]))
    p[0] = p[1]

# Printing

def p_print(p):
    '''
    print : PRINT LPARN args RPARN
    '''
    p[0] = ("print", p[3])
    
def p_args(p):
    '''
    args : expression COMMA args
    '''
    p[0] = [p[1]] + p[3]

def p_args_no(p):
    '''
    args : 
    '''
    p[0] = []

def p_args_last(p):
    '''
    args : expression
    '''
    p[0] = [p[1]]

# List

def p_list(p):
    '''
    list : SLPARN items SRPARN
    '''
    p[0] = ("list", p[2])
    
def p_items(p):
    '''
    items : expression COMMA items
    '''
    p[0] = [p[1]] + p[3]

def p_items_no(p):
    '''
    items : 
    '''
    p[0] = []

def p_items_last(p):
    '''
    items : expression
    '''
    p[0] = [p[1]]

def p_list_func(p):
    '''
    list_funcs : NAME DOT FUNC LPARN args RPARN
    '''
    p[0] = ("list_funcs", p[3], ('var', p[1]), p[5])

def p_list_func_raw(p):
    '''
    list_funcs : list DOT FUNC LPARN args RPARN
    '''
    p[0] = ("list_funcs", p[3], p[1], p[5])

def p_list_index(p):
    '''
    list_index : NAME SLPARN INT SRPARN
    '''
    p[0] = ("list_funcs", "index", ('var', p[1]), [p[3]])

def p_list_index_raw(p):
    '''
    list_index : list SLPARN INT SRPARN
    '''
    p[0] = ("list_funcs", "index", p[1], [p[3]])


# expressions

def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression 
               | expression PLUS expression 
               | expression MINUS expression 
               | expression POWER expression 
               | expression MODULUS expression 
               | expression LESS expression 
               | expression GREATER expression 
               | expression LESSEQUAL expression 
               | expression GREATEREQUAL expression 
               | expression NOTEQUAL expression 
               | expression EQUALEQUAL expression 
               | expression AND expression 
               | expression OR expression 
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_before(p):
    '''
    expression : NOT expression
    '''
    p[0] = (p[1], p[2])

def p_expression_list(p):
    '''
    expression : list_funcs
               | list_index
    '''
    p[0] = p[1]

def p_expression_after(p):
    '''
    expression : expression INCREMENT
               | expression DECREMENT
    '''
    p[0] = (p[2], p[1])

def p_expression_first(p):
    '''
    expression : LPARN expression RPARN
    '''
    p[0] = ('first', p[2])

def p_expression_negative(p):
    '''
    expression : MINUS expression
    '''
    p[0] = ("negative", p[2])
    
def p_expression_single(p):
    '''
    expression : list
               | INT
               | DOUBLE
               | STRING
               | CHAR
               | BOOL
    '''
    p[0] = p[1]

def p_expression_name(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])

# Variables
def p_variable_assign(p):
    '''
    variable_assign : TYPE NAME EQUAL expression
    '''
    p[0] = ("assign", p[1], p[2], p[4])

def p_variable_mutate(p):
    '''
    variable_assign : NAME EQUAL expression
    '''
    p[0] = ("mutate", p[1], p[3])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


### PARSER ###

parser = yacc.yacc()

lang = None

def runFromTerminal():
    global parser
    try:
        lang = input('>>')
    except EOFError:
        print("Program band ho raha hai...")
        return None

    return parser.parse(lang)

def runFromFile(fileName):
    global parser
    lang = ""
    for line in open(fileName):
            lang += line
    return parser.parse(lang)
    
