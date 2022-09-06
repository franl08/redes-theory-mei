
import sys
import os
from ply import lex

tokens = ['DOLLAR', 'DOUBLEDOLLAR', 'ANYTHING']
states = [
    ('inline', 'exclusive'),
    ('block', 'exclusive')
]

def t_ANY_ANYTHING(t):
    r'[^$]+'
    return t

def t_DOUBLEDOLLAR(t):
    r'\${2}'
    t.value = '\\\\[ '
    t.lexer.push_state('block')
    return t

def t_block_DOUBLEDOLLAR(t):
    r'\${2}'
    t.value = ' \\\\]'
    t.lexer.pop_state()
    return t

def t_DOLLAR(t):
    r'\$'
    t.value = r'\\( '
    t.lexer.push_state('inline')
    return t

def t_inline_DOLLAR(t):
    r'\$'
    t.value = r' \\)'
    t.lexer.pop_state()
    return t

def t_ANY_error(t):
    print('Error on file. Changes will not take effect.')
    exit(1)
    
directory = sys.argv[1]
files = os.listdir(directory)

for file in files:
    print(file)
    if (file[-3:] == '.md'):
        file = f'{directory}/{file}'
        f = open(file, 'r')
        f_content = f.read()
        f.close()
        lexer = lex.lex()
        lexer.input(f_content)
        new_text = ''
        for tok in lexer:
            new_text += tok.value
        output = open(file, 'w')
        output.write(new_text)
        output.close()