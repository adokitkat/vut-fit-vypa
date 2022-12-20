import os

from vypa_compiler.internals._utils import eprint, ExitCode, sublist_lookup

symbol_table = []

class Scope:

    def __init__(self):
        self.scope = {}

    def add(self, name, value=None):
        if self.exists(name):
            exit(ExitCode.ERR_SEM_REST) # Redefinition
        self.scope[name] = value

    def set_value(self,name, value):
        if self.exists(name):
            self.scope[name] = value
        else:
            exit(ExitCode.ERR_SEM_REST) # Missing definition

    def lookup(self, name):
        if self.scope.get(name) is None:
            exit(ExitCode.ERR_SEM_REST) # Missing definition

        return self.scope.get(name)

    def exists(self, name):
        return name in self.scope 
    
    def __repr__(self):
        return f"{[(key,type(value)) for key,value in self.scope.items()]}"

class Variable:

    def __init__(self, var_type: str, name: str):
        self.var_type = var_type
        self.name = name

    def __repr__(self):
        return f"Variable: ({self.name=}, {self.var_type=})"

class Function:
    
    def __init__(self, name: str, arguments: list, return_type: str, body, class_this=None):
        self.class_this = class_this
        self.name = name
        self.arguments = []
        self.return_type = return_type
        # For built-in functions arguments don't have to be processed
        if arguments == [] or isinstance(arguments[0], Variable) :
            self.arguments = arguments
        else:
            self.process_function_arguments(arguments)
        self.body = body
        # Built-in functions have no body
        if body:
            self.process_function_body()

    def process_function_arguments(self, sublist):
        if (self.class_this is not None):
            self.arguments.append(self.class_this)
        for arg in sublist:
            self.arguments.append(Variable(var_type=arg[1][1], name=arg[2]))

    def process_function_body(self):
        statements = sublist_lookup(self.body,'statement')
        print("STATEMENTS")
        for statement in statements:
            print(statement)

    def __repr__(self):
        return f"Function: ({self.name=}, {self.return_type=}, args={['this=' + x.name if isinstance(x, Class) else x for x in self.arguments]})"

class Class():

    def __init__(self, name, superclass, class_members):
        self.name = name
        self.superclass = superclass
        self.members = []
        self.symtable = Scope()
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

    # Process int height,width
    def process_next_var(self, next_variables, var_type):
        for var in next_variables:
            x = Variable(var_type=var_type, name=var)
            self.members.append(x)
            # Add variable to class symtable
            self.symtable.add(x.name, x)

    def __repr__(self):
        return f"""Class {self.name}:
{os.linesep.join([f"{' '*8}{repr(x)}" for x in self.members])}"""
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

def add_built_in_functions_to_symtable():
    symbol_table.append(Scope()) # global scope
    symbol_table[0].add(Function(name='readInt', arguments=[], return_type='int', body=None))
    symbol_table[0].add(Function(name='readString', arguments=[], return_type='string', body=None))
    symbol_table[0].add(Function(name='length', arguments=[Variable(var_type='string', name='s')], return_type='int', body=None))
    symbol_table[0].add(Function(name='subStr', arguments=[Variable(var_type='string',name='s'),Variable(var_type='int',name='i'),Variable(var_type='int',name='n')], return_type='string', body=None))
    #Function(name='print',arguments=["?"], return_type='void', body=None)
