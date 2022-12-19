NEW:
program: (function_definition | class_definition)+;

statement
    :   if_else_block
    |   while_block
    |   variable_assignment
    |   instance_assignment
    |   variable_definition
    |   return_statement
    |   expression ';'
    ;

function_definition: function_header function_body;
function_header: variable_type ID '(' parameter_list ')';
function_body: '{' statement* '}';

class_definition: class_header class_body;
class_header: CLASS class_id=ID ':' parent_id=ID;
class_body: '{' class_members* '}';
class_members
    :   field_definition #class_field_definition
    |   function_definition #method_definition;

field_definition: variable_type ID multiple_field_definition* ';';
multiple_field_definition: ',' ID;

// Might be extended with visibility modificators
variable_definition: variable_type ID multiple_variable_definition* ';';
multiple_variable_definition: ',' ID;
variable_assignment: ID '=' expression ';';
instance_assignment: instance_expression '=' expression ';';
return_statement: RETURN expression? ';';

code_block: '{' statement* '}';
if_else_block: if_part else_part;
if_expression: IF '(' expression ')';
if_part: if_expression code_block;
else_part: ELSE code_block;
while_expression: WHILE '(' expression ')';
while_block:  while_expression code_block;

expression
    :   '(' cast=(INT | STRING | ID) ')' expression #castExpression
    |   '(' expression ')'  #bracket_expression
    |   MINUS expression    #negative_expression
    |   '!' expression      #negation_expression
    |   expression operator=('*' | '/') expression #muldiv_expression
    |   expression operator=('+' | MINUS) expression #plusminus_expression
    |   expression operator=(LE | LEQ | GT | GTQ) expression #comparison_expression
    |   expression operator=(LOGICAL_EQUAL | LOGICAL_NEQUAL) expression #equality_expression
    |   expression operator=LOGICAL_AND expression #and_expression
    |   expression operator=LOGICAL_OR expression #or_expression
    |   instance_expression #instance_expression_value
    |   instance_creation   #new_expression
    |   function_call       #function_expression
    |   literal_value       #literal_expression
    |   ID                  #variable_expression;

literal_value
    :   INTEGER_LITERAL
    |   STRING_LITERAL;

# CLASS
first_instance: (reference=(SUPER | THIS | ID) | function_call);
instance_expression: first_instance nested_object;

instance_creation: NEW ID;
nested_object
    :   (final_field_expression | final_method_expression) next_final*;

next_final: (final_field_expression | final_method_expression);

final_field_expression: '.' ID;
final_method_expression: '.' function_call;

function_call: ID '(' expression_list? ')';

expression_list: expression next_expression*;

next_expression
    :   ',' expression;


variable_type: INT | STRING | VOID | ID;
parameter_list
    :   VOID
    |   function_parameters;

function_parameter_definition: variable_type ID;
function_parameters: function_parameter_definition next_parameter*;
next_parameter: ',' function_parameter_definition;





OLD:
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
