#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

import ply.yacc as yacc
from vypa_compiler.internals._utils import eprint
from vypa_compiler.internals._lexer import make_lexer, tokens

"""VYPa Compiler Project 2022

Parser implementation
"""

# TODO

precedence = (

)

def p_expr_list(self,p):
    '''expr_list : expr_list expr
                 | expr'''
 
def p_expr(self,p):
    'expr : e EQUAL'

def p_e(self,p):
    '''e : e PLUS t
         | e MINUS t
         | t'''      
 
def p_t(self,p):
    '''t : LBRACE e RBRACE
         | INT_CONST'''

def p_func_decl(p):
    'func_decl : type ID LPAREN params LPAREN LBRACE stmt RBRACE'

def p_type(p):
    '''type : VOID
            | actual_type'''

def p_actual_type(p):
    '''actual_type : INT 
                   | STRING 
                   | ID'''

def p_params(p):
    '''params : VOID 
              | actual_param'''

def p_actual_param(p):
    'actual_param : actual_type ID multiple_params'

def p_multiple_params(p):
    '''multiple_params : COLON actual_param
                       | empty'''

def p_expression(p):
    pass

def p_stmt(p):
    '''stmt : actual_type ID SEMI
            | actual_type ID EQUALS INT_CONST SEMI
            | actual_type ID EQUALS STRING_CONST SEMI'''

def p_binary_operators(p):
    '''expression : expression PLUS term
                  | expression MINUS term
       term       : term TIMES factor
                  | term DIVIDE factor'''

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : INT_CONST'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    ''
    eprint("Syntax error in input!")

def make_parser():
    parser = yacc.yacc()
    return parser

if __name__ == "__main__":
    #yacc.runmain(vypa_parser)
    pass