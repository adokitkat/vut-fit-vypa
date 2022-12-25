#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

from __future__ import annotations

from vypa_compiler.internals._utils import eprint, ExitCode
from vypa_compiler.internals._models import symbol_table, lookup_in_global_symtable, lookup_variable_in_symtable, Scope, Variable, Function, Class, Program, exists_in_symtable
from vypa_compiler.internals._ast import Node
from vypa_compiler.internals._instructions import Instruction

i = Instruction

binaryOpMap = {
    '*': 'MUL',
    '/': 'DIV',
    '+': 'ADD',
    '-': 'SUB',
    '<': 'LT',
    '>': 'GT',
    '==': 'EQ',
    '&&': 'AND',
    '||': 'OR'
}

PC = '$PC'
SP = '$SP'
FP = '$FP' # $0
PCrestoreR = '$1'
resultR = '$2'
exprR1 = '$3'
exprR2 = '$4'
chunkP = '$5'
miscR1 = '$6'
miscR2 = '$7'

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
    def _start_while() -> str:
        global while_counter
        while_counter += 1 
        while_label = f'WHILE{while_counter}'
        nested_constructions.append(while_label)
        ret = [
                '# Start while',
                i._label(while_label),
            ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _evaluate_while() -> str:
        label = nested_constructions[-1]
        ret = [
            '# Evaluate while',
            __class__._dec_reg(SP),
            i._jumpz(f'{label}__end', f'[{SP}]' )
        ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _cast_int_to_str():
        ret = [
            '# Cast int to string',
            i._create(chunkP, 1),
            i._set_word(chunkP, 0, '""'),
            i._get_word(chunkP, chunkP, 0),
            i._int_to_string(chunkP, f'[{SP} - 1]'),
            i._set(f'[{SP} - 1]', chunkP)
        ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _end_while() -> str:
      label = nested_constructions.pop()
      # Condition
      ret = [
        '# End while',
        i._jump(label),
        i._label(f'{label}__end')
      ]
      return '\n'.join(ret) + '\n'

    #@@staticmethod
    #@def _while(cond, body) -> str:
    #@    ret = [
    #@        __class__._start_while(),
    #@        body,
    #@        __class__._end_while(cond)
    #@    ]
    #@    return '\n'.join(ret) + '\n'

    #_while(cond, process_while_body())
    @staticmethod
    def _if_start() -> str:
        global if_counter
        if_counter += 1
        if_label = f'IF{if_counter}'
        nested_constructions.append(if_counter)
        ret = [
            f'# Start of if',
            __class__._dec_reg(SP),
            i._jumpnz(f'{if_label}', f'[{SP}]'),
            i._jump(f'{if_label}__end'),
            i._label(if_label)          
            ]
        return '\n'.join(ret) + '\n'
    
    @staticmethod
    def _if_end() -> str:
        counter = nested_constructions[-1]
        if_label = f'IF{counter}'
        else_label = f'ELSE{counter}'
        ret = [
            f'# End of if',
            i._jump(f'{else_label}__end'),
            i._label(f'{if_label}__end')
        ]
    
        return '\n'.join(ret) + '\n'

    #_while(cond, process_while_body())
    @staticmethod
    def _if_start() -> str:
        global if_counter
        if_counter += 1
        if_label = f'IF{if_counter}'
        nested_constructions.append(if_counter)
        ret = [
            f'# Start of if',
            __class__._dec_reg(SP),
            i._jumpnz(f'{if_label}', f'[{SP}]'),
            i._jump(f'{if_label}__end'),
            i._label(if_label)          
            ]
        return '\n'.join(ret) + '\n'
    
    @staticmethod
    def _if_end() -> str:
        counter = nested_constructions[-1]
        if_label = f'IF{counter}'
        else_label = f'ELSE{counter}'
        ret = [
            f'# End of if',
            i._jump(f'{else_label}__end'),
            i._label(f'{if_label}__end')
        ]
    
        return '\n'.join(ret) + '\n'
    
    @staticmethod
    def _else_end() -> str:
        counter = nested_constructions.pop()
        else_label = f'ELSE{counter}'
        ret = [
            f'# End of else',
            i._label(f'{else_label}__end')
        ]
        return '\n'.join(ret) + '\n'
        

    @staticmethod
    def _func_call(func_name, args) -> str:
        ret = [f"# Parameters on stack: {args}"]
        ret += [
            f"# Call function: {func_name}",
            i._set(f"[{SP}]", FP), # Save PC to stack
            __class__._inc_reg(SP),
            i._call(f"[{SP}]", func_name) # Call function
        ]

        return_type = lookup_in_global_symtable(func_name).return_type
        if return_type != 'void':
            ret += [
                i._set(f"[{SP}]", resultR), # Save return value to stack
                __class__._inc_reg(SP),
            ]

        return '\n'.join(ret) + '\n'

    @staticmethod
    def _method_call(func_name, args) -> str:
        pass
    
    @staticmethod
    def _var_offset(name) -> str: # TODO:
        if name == 'this':
            return '0'
        
        scope, boolean, offset = exists_in_symtable(name)
        if boolean:
            return f"{list(scope.scope.keys()).index(name) + offset}"
        else:
            return '0'

    @staticmethod
    def _declare_variable(var_type, name) -> str: 
        symbol_table[-1].add(name, Variable(var_type, name))
        ret = [f"# Created variable: {var_type} {name}"]
        if var_type == 'string':
            ret += [
                i._create(chunkP, 1),
                i._set_word(chunkP, 0, '""'),
                i._get_word(chunkP, chunkP, 0),
                i._set(f"[{FP} + {__class__._var_offset(name)}]", chunkP),
                __class__._inc_reg(SP)
            ]
        else: # int variable
            ret += [
                i._set(f"[{FP} + {__class__._var_offset(name)}]", 0),
                __class__._inc_reg(SP)
            ]
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
    def _load_variable(name, stack_offset) -> str:
        ret = [
            f"# Load to variable: {name}, offset: {stack_offset}",
            i._set(
                f"[{FP} + {__class__._var_offset(name)}]",
                *[f"[{SP} + {stack_offset}]" if stack_offset > 0 else f"[{SP} - {abs(stack_offset)}]"]
            )
        ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _return(current_function: str) -> str:
        
        if current_function == 'main':
            return i._jump('__END')
            
        len_params = len(lookup_in_global_symtable(current_function).arguments)
        ret = [
            f"# Expression result to result register",
            i._set(f"{resultR}", f"{exprR1}"),
            f"# Return from: {current_function}",
            i._set(f"{PCrestoreR}", f"[{FP} - 1]"), # Restore program counter value
            i._set(f"{SP}", f"{FP}"), # Restore SP
            i._set(f"{FP}", f"[{FP} - 2]"), # Restore FP
            __class__._dec_reg(SP, 2 + len_params), # Pop parameters from stack
            i._return(f"{PCrestoreR}") # Return to right PC value
        ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _unary_arithmetic_op(op):
        if op == '-':
            ret = [
                f'# Unary arithmetic expression -',
                i._subi(exprR1, 0, f'[{SP} - 1]'),
                i._set(f'[{SP} - 1]', exprR1)
            ]
        else:
            ret = [
                f'# Unary arithmetic expression +',
            ]  
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _binary_operation(op, exprType) -> str:
        if exprType == 'string':
            postfix = 'S'
        else:
            postfix = 'I'
        if op in binaryOpMap.keys():

            if op == '+' and exprType == 'string':
                return __class__._func_call('concat', '2 strings')

            if op in ['||', '&&']:
                logical = f'{binaryOpMap[op]} {exprR1}, [{SP} - 2], [{SP} - 1]'
            else:
                logical = f'{binaryOpMap[op]}{postfix} {exprR1}, [{SP} - 2], [{SP} - 1]'
            ret = [f'# Binary operation {op}',
                    logical,
                    f'SET [{SP} - 2], {exprR1}',
                    __class__._dec_reg(SP) # <----
                ]
        elif op == "<=":
            ret = ['# Binary operation <=',
                    f'LT{postfix} {exprR1}, [{SP} - 2], [{SP} - 1]',
                    f'EQ{postfix} {exprR2}, [{SP} - 2], [{SP} - 1]',
                    f'OR {exprR1}, [{SP} - 2], {exprR1}',
                    __class__._dec_reg(SP)
                    ]
        elif op == ">=":
            ret = ['# Binary operation >=',
                    f'GT{postfix} {exprR1}, [{SP} - 2], [{SP} - 1]',
                    f'EQ{postfix} {exprR2}, [{SP} - 2], [{SP} - 1]',
                    f'OR {exprR1}, {exprR1}, {exprR2}',
                    f'SET [{SP} - 2], {exprR1}',
                    __class__._dec_reg(SP)
                    ]
        elif op == '!=':
            ret = ['# Binary operation!=',
                    f'EQ{postfix} {exprR1}, [{SP} - 2], [{SP} - 1]',
                    f'NOT {exprR1}, {exprR1}',
                    f'SET [{SP} - 2], {exprR1}',
                    __class__._dec_reg(SP)
                    ]
        else:
            eprint('Semantic error')
            exit(ExitCode.ERR_SEM_REST)

        return '\n'.join(ret) + '\n'


    @staticmethod
    def _push_identifier(value) -> str:
        ret = [
            f"# Push identifier {value} to stack",
            i._set(f"[{SP}]", f"[{FP} + {__class__._var_offset(value)}]"),
            __class__._inc_reg(SP)
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
        l = len(parameters)
        ret = [f"# Print: {parameters}"]
        for index, param in enumerate(parameters):
            neg_offset = abs(- l + index)
            if param.name == 'Int-Literal':
                ret += [i._writei(f"[{SP} - {neg_offset}]")]
            
            elif param.name == "String-Literal":
                ret += [i._writes(f"[{SP} - {neg_offset}]")]
            
            elif param.name == 'Identifier':
                lookup = lookup_variable_in_symtable(param.value)
                out_type = lookup.var_type
                if out_type == 'string':
                    ret += [i._writes(f"[{SP} - {neg_offset}]")]
                else:
                    ret += [i._writei(f"[{SP} - {neg_offset}]")]
            
            elif param.type == 'Binary':
                if param.left.value is not None:
                    if param.left.name == 'Int-Literal':
                        ret += [i._writei(f"[{SP} - {neg_offset}]")]
                    elif param.left.name == 'String-Literal':
                        ret += [i._writes(f"[{SP} - {neg_offset}]")]
                    elif param.left.name == 'Identifier':
                        lookup = lookup_variable_in_symtable(param.left.value)
                        out_type = lookup.var_type
                        if out_type == 'string':
                            ret += [i._writes(f"[{SP} - {neg_offset}]")]
                        else:
                            ret += [i._writei(f"[{SP} - {neg_offset}]")]

            elif param.name == 'Function-call':
                lookup = lookup_in_global_symtable(param.value)
                out_type = lookup.return_type
                if out_type == 'string':
                    ret += [i._writes(f"[{SP} - {neg_offset}]")]
                else:
                    ret += [i._writei(f"[{SP} - {neg_offset}]")]

        ret += [i._subi(SP, SP, len(parameters))]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _read_int_stack() -> str:
        ret = [
            #f"# Function: Read int from stdin and put to stack",
            #i._label("ReadIntToStack"),
            i._readi(miscR1),
            i._set(f"[{SP}]", miscR1),
            __class__._inc_reg(SP),
            #i._set(f"[{SP} - 1]", miscR1),
            #i._return(f"[{SP}]")
        ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _read_string_stack() -> str:
        ret = [
            f"# Function: Read string from stdin and put to stack",
            #i._label("ReadStringToStack"),
            i._reads(miscR1),
            i._set(f"[{SP}]", miscR1),
            __class__._inc_reg(SP),
            #i._set(f"[{SP} - 1]", miscR1),
            #i._return(f"[{SP}]")
        ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _length() -> str:
        ret = [
            f"# Length function",
            i._label("length"),
            i._get_size(miscR1, f'[{SP} - 2]'),
            i._subi(SP, SP, 1),
            i._set(resultR, miscR1),
            i._return(f'[{SP} + 1]')
            ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _concat() -> str:
        ret = [
            i._label("concat"),
            i._get_size(exprR1, f'[{SP} - 3]'), # string 1
            i._get_size(exprR2, f'[{SP} - 2]'), # string 2
            i._copy(chunkP, f'[{SP} - 3]'),
            i._addi(miscR2, exprR1, exprR2), # total length
            i._resize(chunkP, miscR2),
            i._set(resultR, 0),
            i._label("concat_start"),
            i._lti(miscR2, resultR, exprR2),
            i._jumpz("concat_end", miscR2),
            i._get_word(miscR2, f'[{SP} - 2]', resultR),
            i._addi(miscR1, resultR, exprR1),
            i._set_word(chunkP, miscR1, miscR2),
            __class__._inc_reg(resultR),
            i._jump("concat_start"),
            i._label("concat_end"), 
            __class__._dec_reg(SP, 3),
            i._set(resultR, chunkP),
            #__class__._inc_reg(SP),
            i._return(f'[{SP} + 3]')
        ]
        return '\n'.join(ret) + '\n'

    @staticmethod
    def _substring() -> str: # TODO: $1 -> miscR2 ; $2 -> resultR
        ret = [
            f"# Substring function",
            i._label('subStr'),
            i._get_size(miscR1, f'[{SP} - 4]'),
            i._gti(exprR1, f'[{SP} - 3]', miscR1),
            i._lti(exprR2, f'[{SP} - 3]', 0),
            i._or(exprR1, exprR1, exprR2),
            i._jumpz('__substr_start', exprR1),
            i._create(chunkP, 1),
            i._set_word(chunkP, 0, '""'),
            i._get_word(chunkP, chunkP, 0),
            i._jump("substr_end"),

            i._label("__substr_start"),
            i._create(chunkP, f'[{SP} - 2]'),
            i._set(exprR1, f'[{SP} - 3]'),
            i._set(resultR, 0),
            i._addi(miscR2, exprR1, f'[{SP} - 2]'),
            i._lti(miscR2, miscR2, miscR1),
            i._jumpnz('substr_start', miscR2),
            i._subi(miscR2, miscR1, exprR1),

            i._resize(chunkP, miscR2),

            i._label('substr_start'),
            i._lti(miscR2, exprR1, miscR1),
            i._jumpz('substr_end', miscR2),

            i._lti(miscR2, resultR, f'[{SP} - 2]'), # TODO: $1 -> miscR2 ; $2 -> resultR
            i._jumpz('substr_end', miscR2),

            i._get_word(miscR2, f'[{SP} - 4]', exprR1),
            i._set_word(chunkP, resultR, miscR2),

            __class__._inc_reg(resultR),
            __class__._inc_reg(exprR1),
            i._jump('substr_start'),
            i._label('substr_end'),

            __class__._dec_reg(SP, 4),
            #i._set(f'[{SP}]', chunkP),
            i._set(resultR, chunkP),
            #__class__._inc_reg(SP),
            i._return(f'[{SP} + 4]')
        ]
        return '\n'.join(ret) + '\n'