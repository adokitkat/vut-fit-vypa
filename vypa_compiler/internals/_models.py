#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

from __future__ import annotations

import os

from vypa_compiler.internals._utils import eprint, ExitCode, sublist_lookup

symbol_table = []


def sematic_type_check(expected_type, type):
    if expected_type != type: 
        eprint(f"Incompatible assign value, expected {expected_type}, got {type}")
        exit(ExitCode.ERR_SEM_TYPE_INCOMP) # Incompatible type

# Checks for sematic assign error
def sematic_check_assign(ast):
	left_type = lookup_variable_in_symtable(ast.left.value).var_type
	right_type = sematic_check_expr(ast.right)
	sematic_type_check(left_type, right_type)

# Checks type of expression
def sematic_check_expr(ast):
	if ast.type == 'Unary':
		return 'int'
	elif ast.type == 'Binary':
		left_type = sematic_check_expr(ast.left)
		right_type = sematic_check_expr(ast.right)
		sematic_type_check(left_type,right_type)
		return left_type
	elif ast.name == 'Int-Literal':
		return 'int'
	elif ast.name == 'String-Literal':
		return 'string'
	elif ast.name == 'Identifier':
		return lookup_variable_in_symtable(ast.value).var_type
	elif ast.name == 'Function-call':
		function = lookup_in_global_symtable(ast.value)
		sematic_func_call_arguments_check(function, ast)
		return function.return_type
	elif ast.name == 'Expression-cast':
		return ast.left.value
	
# Checks the type and number of arguments in function call
def sematic_func_call_arguments_check(function, ast):
    if ast.right:
        arguments_in_call = sematic_get_function_arguments_type(ast.right)
    else:
        arguments_in_call = []
    arguments_in_function = []
    for argument in function.arguments:
        arguments_in_function.append(argument.var_type)
    for type1,type2 in zip(arguments_in_call, arguments_in_function):
        if type1 != type2:
            eprint(f"Incompatible argument type in function {function.name}, expected {type2}, got {type1}")
            exit(ExitCode.ERR_SEM_TYPE_INCOMP) # Incompatible type
	
# Helper function to get argument types of called function
def sematic_get_function_arguments_type(ast):
    parameters = []
    if ast.name == 'Expression-list' or ast.name == 'Next-expression':
        parameter = sematic_check_expr(ast.left)
        if parameter is not None:
            parameters.append(parameter)
        if ast.right:
            returned_parameters = sematic_get_function_arguments_type(ast.right)
            if returned_parameters is not None:
                parameters += returned_parameters
    return parameters

# Sematic check if returned type equals return type of the function
def sematic_check_return_type(function,ast):
    return_type = sematic_check_expr(ast.left)
    if return_type != function.return_type:
        eprint(f"Incompatible return value, expected {function.return_type}, got {return_type}")
        exit(ExitCode.ERR_SEM_TYPE_INCOMP) # Incompatible type

# Lookup in global symtable for functions and classes
def lookup_in_global_symtable(name):
    lookup = symbol_table[0].lookup(name)
    if lookup is not None:
        return lookup
    else:
        eprint(f"Missing definition (global): {name}")
        exit(ExitCode.ERR_SEM_REST) # Missing definition

# Lookup in local symtables for variables
def lookup_variable_in_symtable(name):
    for scope in reversed(symbol_table):
        if scope is symbol_table[0]: # We don't want to search in global scope for variables
            continue
        lookup = scope.lookup(name)
        if lookup is not None:
            return lookup
    
    eprint(f"Missing definition: {name}")
    exit(ExitCode.ERR_SEM_REST) # Missing definition

# Checks if a variable exists in the scope and returns offset and the scope
def exists_in_symtable(name):
    offset = 0
    found = False
    found_scope = None
    for scope in reversed(symbol_table):
        # End of search
        if scope == symbol_table[0]:
            return found_scope, found, offset
        # Found, compute offset
        if found == True:
            offset += len(scope.scope.keys())
        if scope.exists(name):
            found = True
            found_scope = scope

# Represents scope
class Scope:

    def __init__(self):
        self.scope = {}

    def add(self, name, value=None) -> bool:
        if self.exists(name):
            eprint(f"Redefinition of: {name}")
            exit(ExitCode.ERR_SEM_REST) # Redefinition
        self.scope[name] = value
        return True

    def set_value(self,name, value) -> bool:
        if self.exists(name):
            self.scope[name].value = value
            return True
        else:
            return False

    def lookup(self, name):
        return self.scope.get(name)

    def exists(self, name) -> bool:
        return name in self.scope 
    
    def __repr__(self):
        return f"{[(key,type(value)) for key,value in self.scope.items()]}"

# Represents a variable
class Variable:

    def __init__(self, var_type: str, name: str):
        self.var_type = var_type
        self.name = name
        self.value = None

    def __repr__(self):
        return f"Variable: ({self.name=}, {self.var_type=})"

# Represents a function
class Function:
    
    def __init__(self, name: str, arguments: list, return_type: str, body, class_this=None):
        self.class_this = class_this
        self.name = name
        self.arguments = []
        self.return_type = return_type
        self.generated = False
        # For built-in functions arguments don't have to be processed
        if arguments == [] or isinstance(arguments[0], Variable) :
            self.arguments = arguments
        else:
            self.process_function_arguments(arguments)
        self.body = body

    def mark_generated(self):
        self.generated = True
        
    def is_generated(self) -> bool:
        return self.generated

    def process_function_arguments(self, sublist):
        if (self.class_this is not None):
            self.arguments.append(self.class_this)
        for arg in sublist:
            self.arguments.append(Variable(var_type=arg[1][1], name=arg[2]))

    def __repr__(self):
        return f"Function: ({self.name=}, {self.return_type=}, args={['this=' + x.name if isinstance(x, Class) else x for x in self.arguments]})"

# Represents a class
class Class():

    def __init__(self, name, superclass, class_members):
        self.name = name
        self.superclass = superclass
        self.symtable = Scope()
        
        this = Variable(name, 'this')
        
        if superclass is not None:
            _super = Variable(superclass, 'super')
        else:
            _super = Variable(None, 'super')
        self.members = [this, _super]
        self.symtable.add(this.name, this)
        self.symtable.add(_super.name, _super)
        self.process_class_members(class_members)
    
    # Process functions and variables in the class
    def process_class_members(self, class_members):
        for class_member in class_members:
            if class_member[0] == 'variable-definition':
                x = Variable(var_type=class_member[1][1], name=class_member[2])
                self.members.append(x)
                # Add variable to class symtable
                self.symtable.add(x.name, x)
                self.process_next_var(sublist_lookup(class_member,'next-var'),var_type=class_member[1][1])
            
            if class_member[0] == 'function-definition':
                x = Function(name=class_member[1][2], arguments=sublist_lookup(class_member, 'function-parameters'), return_type=class_member[1][1][1], body=sublist_lookup(class_member, 'function-body') ,class_this=self)
                self.members.append(x)
                # Add function to class symtable
                self.symtable.add(x.name, x)

    def process_next_var(self, next_variables, var_type):
        for var in next_variables:
            x = Variable(var_type=var_type, name=var)
            self.members.append(x)
            # Add variable to class symtable
            self.symtable.add(x.name, x)

    def __repr__(self):
        return f"""Class {self.name}:
{os.linesep.join([f"{' '*8}{repr(x)}" for x in self.members])}"""

# Represents a program
class Program:

    def __init__(self, parsed_list):
        self.parsed_list = parsed_list
        self.classes = []
        self.functions = []
        self.traverse_programs(sublist_lookup(self.parsed_list, 'program'))
        
    def traverse_programs(self, programs):
        for program in programs:
            if program[0] == "class-definition":
                self.process_class(program)
            elif program[0] == "function-definition":
                self.process_function(program)

    def process_class(self, class_sublist):
        x = Class(class_sublist[1], class_sublist[2], sublist_lookup(class_sublist, 'class-member-definition'))
        self.classes.append(x)
        symbol_table[0].add(x.name, x)

    def process_function(self, function_sublist):
        x = Function(name=function_sublist[1][2], arguments=sublist_lookup(function_sublist, 'function-parameters'), return_type=function_sublist[1][1][1], body=sublist_lookup(function_sublist, 'function-body'))
        self.functions.append(x)
        symbol_table[0].add(x.name, x)

    def __repr__(self):
        return f"""Program:
{os.linesep.join([f"{' '*4}{repr(x)}" for x in self.classes])}
{os.linesep.join([f"{' '*4}{repr(x)}" for x in self.functions])}"""

# Adds built-in functions to the global symtable
def add_built_in_functions_to_symtable():
    if not symbol_table[0].exists('readInt'):
        symbol_table[0].add('readInt', Function(name='readInt', arguments=[], return_type='int', body=None))
    if not symbol_table[0].exists('readString'):
        symbol_table[0].add('readString', Function(name='readString', arguments=[], return_type='string', body=None))
    if not symbol_table[0].exists('length'):
        symbol_table[0].add('length', Function(name='length', arguments=[Variable(var_type='string', name='s')], return_type='int', body=None))
    if not symbol_table[0].exists('subStr'):
        symbol_table[0].add('subStr', Function(name='subStr', arguments=[Variable(var_type='string', name='s'), Variable(var_type='int', name='i'), Variable(var_type='int',name='n')], return_type='string', body=None))
    if not symbol_table[0].exists('concat'):
        symbol_table[0].add('concat', Function(name='concat', arguments=[Variable(var_type='string', name='s1'), Variable(var_type='string', name='s2')], return_type='string', body=None))
    