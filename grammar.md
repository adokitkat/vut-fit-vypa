Parenteses ()
brackets []
braces {}

# class Rectange : Object { int id; void Shape(void) {statement}}
class: CLASS ID COLON ?SUPERCLASS? LBRACE classdef RBRACE

# int id | void Shape(void) {statement}
classdef: defvar classdef
        | decl_function classdef
        | EMPTY

# Deklaracia funkcie void main(void) {...}
decl_function: type ID LPAREN params RPAREN LBRACE statement RBRACE

# Typ void | not void typy
type: VOID
    | not_void_type

# Not void typy (ID - Object type)
not_void_type: INT
    | STRING
    | ID 

# Parametre: buď VOID | int a, string b
params: VOID
    | not_void_param

# int a, string b
not_void_param: not_void_type ID multiple_params

#  , 
multiple_params: COMMA not_void_param
    | EMPTY

# Deklarácia | funckia | If else | While
statement: defvar statement 
        | ID assignment_expr SEMI statement
        | expr SEMI statement
        | IF expr LBRACE statement RBRACE else statement
        | WHILE expr LBRACE statement RBRACE statement
        | RETURN expr SEMI ?statement?
        | EMPTY

# int a, res;
defvar: not_void_type ID more_vars assignment_expr SEMI

# int a, res;
more_vars: COMMA ID more_vars
    | EMPTY

# = expr
assignment_expr: EQUALS expr
    | EMPTY

# else {statement}
else: ELSE LBRACE statement RBRACE
    | EMPTY

# Fuck my life - lol
# An expression consists of integer and string literals, local variables, instance variables, brackets, function/method calls, object creation, context object, casting, and arithmetic, logic, and relation operators. The binary arithmetic and logic operators are left associative. The complete list of operators with precedence/priorities (the highest at the first row) is in Table 1, where Types column uses the following abbreviations: N = int, T = data_type, P = prim_type, and NC = int or object type. These operators are described in more details in the remainder of this section.
expr: 