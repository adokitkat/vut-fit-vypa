#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

import ply.yacc as yacc
from vypa_compiler.internals._utils import eprint, ExitCode
from vypa_compiler.internals._lexer import make_lexer, tokens

"""VYPa Compiler Project 2022

Parser implementation
"""

# TODO

precedence = (
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'LNOT'),
    ('left', 'PERIOD'),
    ('nonassoc', 'LPAREN', 'RPAREN'),
    ('nonassoc', 'NEW')
)

def p_start(p):
    """start : program"""
    p[0] = ("start", p[1])

def p_program(p):
    '''program : func_def program
               | class_def program
               | empty''' 
    if len(p) == 3:
        p[0] = ("program", p[1], p[2])

def p_empty(p):
    'empty :'
    pass

# FUNCTION DEFINITION
def p_func_def(p):
    '''func_def : func_header func_body'''
    p[0] = ("function-definition", p[1], p[2])

def p_func_header(p):
    '''func_header : var_type ID LPAREN param_list RPAREN'''
    p[0] = ("function-header", p[1], p[2], p[4])

def p_func_body(p):
    '''func_body : statement_new_scope'''
    p[0] = ("function-body", p[1])

def p_param_list(p):
    '''param_list : VOID
                  | func_param'''
    p[0] = ("function-parameter-list", p[1])

def p_func_param(p):
    '''func_param : func_param_def next_param'''
    p[0] =  ("function-parameters", p[1], p[2])

def p_func_param_def(p):
    '''func_param_def : var_type ID'''
    p[0] = ("function-parameter-definition", p[1], p[2])

def p_next_param(p):
    '''next_param : COMMA func_param
                  | empty'''
    if len(p) == 3:
        p[0] = ("function-next-parameter", p[2])
    else:
        p[0] = ("function-next-parameter", None)

# CLASS DEFINITION
def p_class_def(p):
    '''class_def : CLASS ID COLON ID class_body'''
    p[0] = ("class-definition", p[2], p[4], p[5])

def p_class_body(p):
    '''class_body : LBRACE class_member_list RBRACE'''
    p[0] = ("class-body", p[2])

# ("class" , "definition" , int id, void Shape, string toString, None
def p_class_member_list(p):
    '''class_member_list : class_member'''
    p[0] = ("class-member-list", p[1])

def p_class_member_list_none(p):
    '''class_member_list : empty'''
    p[0] = ("class-member-list", None)

def p_class_member(p):
    '''class_member : class_member_def class_next_member'''
    p[0] = ("class-members", p[1], p[2])

def p_class_member_def(p):
    '''class_member_def : var_def
                        | func_def'''
    p[0] = ("class-member-definition", p[1])

def p_class_next_member(p):
    '''class_next_member : class_member'''
    p[0] = ("class-next-member", p[1])

def p_class_next_member_none(p):
    '''class_next_member : empty'''
    p[0] = ("class-next-member", None)
    
# VARIABLE TYPE TODO: REMOVE VOID? 
def p_var_type(p):
    '''var_type : INT
                | STRING
                | VOID
                | ID'''
    p[0] = ("var-type", p[1])

# STATEMENTS
def p_statement(p): # TODO
    '''statement : var_def statement
                 | var_assignment statement
                 | statement_expr statement
                 | statement_return statement
                 | statement_while statement
                 | statement_if statement
                 | statement_this statement
                 | statement_id statement
                 | empty '''
    if len(p) == 3:
        p[0] = ("statement", p[1], p[2])
    else:
        p[0] = None

def p_statement_new_scope(p):
    '''statement_new_scope : LBRACE statement RBRACE statement_scope_end'''
    p[0] = ("statement-scope",  p[2], p[4])

def p_statement_scope_end(p):
    '''statement_scope_end : empty'''
    p[0] = ("statement-scope-end", None)
#      # Action code
#      ...
#      pop_scope()        # Return to previous scope
 
# def p_new_scope(p):
#     '''new_scope :'''
#     p[0] = ("new-scope")
#      # Create a new scope for local variables
#      s = new_scope()
#      push_scope(s)
#      ...

def p_if_statement(p):
    '''statement_if : IF LPAREN expr RPAREN statement_new_scope ELSE statement_new_scope'''
    p[0] = ("statement-if", p[3], p[5], p[7])

def p_while_statement(p):
    '''statement_while : WHILE LPAREN expr RPAREN statement_new_scope'''
    p[0] = ("statement-while", p[3], p[5])

def p_statement_return(p):
    '''statement_return : RETURN expr SEMI'''
    p[0] = ("statement-return", p[2])

def p_statement_this(p):
    '''statement_this : THIS PERIOD ID EQUALS expr SEMI'''
    p[0] = ("statement-this-assignment", p[3], p[5])

"""
class A {
    int a;
    void bar() { print("bar"); }
    void foo(int x) {
        int h;
        h = this.a;
        this.bar();
        this.a = x;
    }
}
"""

def p_statement_id(p):
    '''statement_id : ID PERIOD ID EQUALS expr SEMI'''
    p[0] = ("statement-id", p[1], p[3], p[5])
    
def p_statement_expr(p):
    '''statement_expr : expr SEMI'''
    p[0] = ("statement-expr", p[1])

def p_var_assignment(p):
    'var_assignment : ID EQUALS expr SEMI'
    p[0] = ("variable-assigment", p[1], p[3])

# DEFVAR
def p_var_def(p):
    'var_def : var_type ID multiple_var_def' 
    p[0] = ("variable-definition", p[1], p[2], p[3])

def p_multiple_var_def(p):
    '''multiple_var_def : SEMI
                        | COMMA ID multiple_var_def
    '''
    if len(p) == 4:
        p[0] = ('next-var', p[2], p[3])

################ EXPRESSIONS #################
def p_expr_paren(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = ("expression-parentheses", p[2])

def p_expr_value_id(p):
    '''expr : ID'''
    p[0] = ("expression-value", 'identifier', p[1])

def p_expr_value_int(p):
    '''expr : INT_CONST'''
    p[0] = ("expression-value", 'int', p[1])

def p_expr_value_string(p):
    '''expr : STRING_CONST'''
    p[0] = ("expression-value", 'string', p[1])
    

def p_expr_arithmetic_operation_unary(p):
    '''expr : MINUS expr'''
    p[0] = ("expression-arithmetic-unary", p[1], p[2])#p[2], p[1]), p[3]) # ???

def p_expr_arithmetic_operation(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr'''
    p[0] = ("expression-arithmetic-binary",p[2], p[1], p[3])# p[1], p[3], p[2]) # 

def p_expr_logical_operation_unary(p):
    '''expr : LNOT expr'''
    p[0] = ("expression-logical-unary", p[1], p[2])

def p_expr_logical_operation(p):
    '''expr : expr LOR expr
            | expr LAND expr'''
    p[0] = ("expression-logical-binary", p[2], p[1], p[3]) # Možno zmeniť na postfix?

def p_expr_relational_operation(p):
    '''expr : expr LT expr
            | expr LE expr
            | expr GE expr
            | expr GT expr
            | expr EQ expr
            | expr NE expr'''
    p[0] = ("expression-relational", p[2], p[1], p[3])
            
def p_expr_cast(p):
    '''expr : LPAREN INT RPAREN expr
            | LPAREN STRING RPAREN expr'''
    p[0] = ("expression-cast", p[2], p[4])

# new Rectangle, this.id, rec.value(), this.value(), super.value()
def p_expr_class_new(p):
    '''expr : NEW ID'''
    p[0] = ("expression-class-new", p[2])

def p_expr_class_operations(p):
    '''expr : ID PERIOD expr
            | THIS PERIOD expr
            | SUPER PERIOD expr'''
    p[0] = ("expression-class-op", p[1], p[3])

def p_expr_function_call(p):
    '''expr : ID LPAREN expr_list RPAREN
            | ID LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = ("expression-function-call", p[1], p[3])
    else:
        p[0] = ("expression-function-call", p[1], None)

# value(a,)
def p_expr_list(p): 
    '''expr_list : expr next_expr'''
    p[0] = ("expression-list", p[1], p[2])

def p_next_expr(p):
    '''next_expr : COMMA expr_list
                 | empty'''
    if len(p) == 3:
        p[0] = ("next-expression", p[2])
    else:
        p[0] = None

def p_error(p):
    ''''''
    eprint("Syntax error in input! | Type: %s | Value: %s" % (p.type, p.value))
    exit(ExitCode.ERR_SYN)

def make_parser():
    parser = yacc.yacc(tabmodule="parse_table", outputdir="vypa_compiler/generated")
    return parser

if __name__ == "__main__":
    #yacc.runmain(vypa_parser)
    pass