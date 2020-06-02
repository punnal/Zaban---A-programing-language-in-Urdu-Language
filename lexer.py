import ply.lex as lex

tokens = [
    'PRINT',

    'EQUAL',

    'INT',
    'DOUBLE',
    'CHAR',
    'STRING',
    'BOOL',

    'NAME',

    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'POWER',
    'MODULUS',
    'INCREMENT',
    'DECREMENT',

    'LESS',
    'GREATER',
    'LESSEQUAL',
    'GREATEREQUAL',
    'NOTEQUAL',
    'EQUALEQUAL',
    'NOT',
    'AND',
    'OR',

    'LPARN',
    'RPARN',

    'COMMA',

    'END',

    'DO',
    'WHILE',
    'CLPARN',
    'CRPARN',
    'BREAK',
    'CONTINUE',

    'SLPARN',
    'SRPARN',

    'TYPE',

    'DOT',
    'FUNC',
    #'POP',
    #'PUSH',
    #'INDEX',
    #'SLICE'

]


t_ignore = ' \t'

t_DOT = r'\.'

t_INCREMENT = r'\+\+'
t_DECREMENT = r'\-\-'

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY= r'\*'
t_DIVIDE = r'\/'

t_POWER = r'\^'
MODULUS = r'\%'

t_LESS = r'\<'
t_GREATER = r'\>'
t_LESSEQUAL = r'\<\='
t_GREATEREQUAL = r'\>\='
t_NOTEQUAL = r'\!\='
t_EQUALEQUAL = r'\=\='

t_EQUAL = r'\='

t_LPARN = r'\('
t_RPARN = r'\)'

t_CLPARN = r'\{'
t_CRPARN = r'\}'

t_SLPARN = r'\['
t_SRPARN = r'\]'

t_COMMA = r'\,'

t_END = r'\;'


### LEXER ###

def t_PRINT(t):
    r'chapo'
    return t

def t_NOT(t):
    r'not'
    return t

def t_AND(t):
    r'and'
    return t

def t_OR(t):
    r'or'
    return t

def t_DO(t):
    r'karo'
    return t

def t_WHILE(t):
    r'jabtak'
    return t

def t_FUNC(t):
    r'(pop)|(push)|(index)|(slice)'
    return t

def t_BREAK(t):
    r'toro'
    return t

def t_CONTINUE(t):
    r'jariRakho'
    return t

def t_TYPE(t):
    r'(int)|(double)|(char)|(string)|(bool)|(list)'
    if(t.value == 'list'):
        t.value = list
    if(t.value == 'int'):
        t.value = int
    elif(t.value == 'double'):
        t.value = float
    elif(t.value == 'string'):
        t.value = str
    elif(t.value == 'bool'):
        t.value = bool
    elif(t.value == 'char'):
        t.value = str
    return t

def t_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR(t):
    r'\'.\''
    t.value = t.value[1]
    return t

def t_STRING(t):
    r'\"[^"]*\"'
    t.value = t.value[1:-1]
    return t

def t_BOOL(t):
    r'(darust)|(ghalat)'
    if t.value == 'darust':
            t.value = True
    else:
            t.value = False
    return t

def t_NAME(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    #print("SyntaxError: ", "Line: " , t.lexer.lineno,"Ghair Kanooni lafz: '%s'" %t.value[0])
    raise SyntaxError("lexer", t.lexer.lineno, t.value[0])
    #t.lexer.skip(1)

lexer = lex.lex()

