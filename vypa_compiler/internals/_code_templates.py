#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

from vypa_compiler.internals._models import symbol_table, lookup_in_global_symtable, lookup_variable_in_symtable, Scope, Variable, Function, Class, Program, exists_in_symtable
from vypa_compiler.internals._ast import Node
from vypa_compiler.internals._instructions import Instruction

i = Instruction

SP = '$SP'
FP = '$FP'
PC = '$PC'
expressionResultReg1 = '$4'
expressionResultReg2 = '$5'
chunkP = '$6'
miscR = '$7'

while_counter = 0 
if_counter = 0
nested_constructions = []

class CodeTemplate:

    # Templates for code generation
    @staticmethod
    def _inc_reg(reg, value=1) -> str:
        return i._addi(reg, reg, value)

    @staticmethod
    def _dec_reg(reg, value=1) -> str:
        return i._subi(reg, reg, value)

    @staticmethod
    def _if_else(cond, if_code, else_code) -> str:
        pass

    @staticmethod
    def _start_while() -> str:
        while_counter += 1 
        while_label = f'WHILE{while_counter}'
        nested_constructions.append(while_label)
        return i._label(while_label)
        

    @staticmethod
    def _end_while(cond) -> str:
      label = nested_constructions.pop()
      # Condition
      ret = [
        i._jump(label),
        i._label(label + "_end")
      ]
      return '\n'.join(ret) + '\n'

    @staticmethod
    def _while(cond, body) -> str:
        ret = [
            __class__._start_while(),
            body,
            __class__._end_while(cond)
        ]
        return '\n'.join(ret) + '\n'

    #_while(cond, process_while_body())

    @staticmethod
    def _func_call(func_name, args) -> str:
        ret = [
            f"# Call function: {func_name}",
            i._set(f"[{SP}]", PC), # Save PC to stack
            __class__._inc_reg(SP),
            i._call(f"[{SP}]", func_name) # Call function
        ]
        return ret + '\n'

    @staticmethod
    def _method_call(func_name, args) -> str:
        pass
    
    @staticmethod
    def _var_offset(name) -> str: # TODO:
        if name == 'this':
            pass
        if exists_in_symtable(name):
            return f"{list(symbol_table[-1].scope.keys()).index(name)}"
        else:
            pass

    @staticmethod
    def _declare_variable(var_type, name) -> str: 
        symbol_table[-1].add(name, Variable(var_type, name))
        ret = [f"# Created variable: {name}"]
        if var_type == 'string':
            ret += [
                i._create(chunkP, 1),
                i._set_word(chunkP, 0, '""'),
                i._get_word(chunkP, chunkP, 0),
                i._set(f"[{FP} + {__class__._var_offset(name)}]", chunkP),
            ]
        else: # int variable
            ret += [i._set(f"[{FP} + {__class__._var_offset(name)}]", 0)]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _assign_variable(name) -> str:
        ret = [
            f"# Assign to variable: {name}",
            __class__._dec_reg(SP),
            i._set(f"[{FP} + {__class__._var_offset(name)}]", f"[{SP}]")
        ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _literal_int(value) -> str: 
        ret = [
            f"# Create int literal: {value}",
            i._set(f"[{SP}]", value),
            __class__._inc_reg(SP)
        ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _literal_string(value) -> str: 
        ret = [
            f"# Create string literal: {value}",
            i._create(chunkP, 1),
            i._set_word(chunkP, 0, f'"{value}"'),
            i._get_word(chunkP, chunkP, 0),
            i._set(f"[{SP}]", chunkP),
            __class__._inc_reg(SP)
        ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _print(parameters) -> str: 
        l = len (parameters)
        print(">>> params in print:", parameters)
        ret = [f"# Print: {parameters}"]
        for index, param in enumerate(parameters):
            if param.name == 'Int-Literal':
                ret += [i._writei(f"[{SP} - {-index + l}]")]
            elif param.name == "String-Literal":
                ret += [i._writes(f"[{SP} - {-index + l}]")]
            elif param.name == 'Identifier':
                var_type = lookup_variable_in_symtable(param.value).var_type
                if var_type == 'string':
                    ret += [i._writes(f"[{FP} + {__class__._var_offset(param.value)}]")]
                else:
                    ret += [i._writei(f"[{FP} + {__class__._var_offset(param.value)}]")]
        return '\n'.join(ret) + '\n'


    # TODO: treba??
    @staticmethod
    def _read_int_stack() -> str:
        ret = [
            #f"# Function: Read int from stdin and put to stack",
            #i._label("ReadIntToStack"),
            i._readi(miscR),
            i._set(f"[{SP}]", miscR),
            __class__._inc_reg(SP),
            #i._set(f"[{SP} - 1]", miscR),
            #i._return(f"[{SP}]")
        ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _read_string_stack() -> str:
        ret = [
            f"# Function: Read string from stdin and put to stack",
            #i._label("ReadStringToStack"),
            i._reads(miscR),
            i._set(f"[{SP}]", miscR),
            __class__._inc_reg(SP),
            #i._set(f"[{SP} - 1]", miscR),
            #i._return(f"[{SP}]")
        ]
        return '\n'.join(ret) + '\n'
    