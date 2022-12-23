#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

import re

import ply.lex as lex

from vypa_compiler.internals._utils import eprint, ExitCode

"""VYPa Compiler Project 2022

Lexer implementation
"""

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

t_ignore = ' '

# Reserved keywords
reserved = (
    "CLASS", "ELSE", "IF", "INT", "NEW", "RETURN", "STRING", "SUPER", "THIS", "VOID", "WHILE"
)

tokens = reserved + (
    # Literals
    "ID", "INT_CONST", "STRING_CONST",

    # Operators
    # +, -, *, /
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    # !, ||, &&
    'LNOT', 'LOR', 'LAND',
    # <, <=, >, >=, ==, !=
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # Assignment
    'EQUALS', 

    # Delimeters
    'LPAREN', 'RPAREN',
    # 'LBRACKET', 'RBRACKET', # Isn't needed
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON',
)

def t_INT_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_CONST(t):
    r'((?<!\\)"[^"\\]*(?:\\.[^"\\]*)*")' # This one doesn't work with escaped \" -> " r'\"[\n\t\"\x20-\x21\x23-\U0010FFFF]*?\"'
    t.value = t.value[1:-1]
    return t

t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'

t_LNOT = r'!'
t_LOR  = r'\|\|'
t_LAND = r'&&'

t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

t_EQUALS = r'='

t_LPAREN   = r'\('
t_RPAREN   = r'\)'
#t_LBRACKET = r'\['
#t_RBRACKET = r'\]'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_COMMA    = r','
t_PERIOD   = r'\.'
t_SEMI     = r';'
t_COLON    = r':'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r

def t_ID(t):
    r'[A-Za-z_][a-zA-Z0-9_]*'
    t.type = reserved_map.get(t.value, "ID") # If not reserved, then identifier
    return t

def t_MULTI_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_COMMENT(t):
    r'//.*'
    #t.lexer.lineno += 1
    pass

def t_error(t):
    eprint('Lexical error | Line: %d | Symbol: %s | %s' % (t.lineno, repr(t.value[0]), find_column(t.value[0], t))) 
    #t.lexer.skip(1)
    # TODO: Use t.lexer.lineno to indicade line number of illegal input input?
    #       Quit after error and return ERR_LEX?
    exit(ExitCode.ERR_LEX)

def make_lexer():
     lexer = lex.lex(reflags=re.UNICODE|re.VERBOSE)
     return lexer

if __name__ == "__main__":
    lex.runmain(make_lexer())