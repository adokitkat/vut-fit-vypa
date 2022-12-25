#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

"""VYPa Compiler Project 2022

Main source file
"""

import os, sys

from vypa_compiler.internals._utils import eprint, ExitCode
from vypa_compiler.internals._lexer import make_lexer
from vypa_compiler.internals._parser import make_parser
from vypa_compiler.internals._models import symbol_table, add_built_in_functions_to_symtable, Program, Scope
from vypa_compiler.internals._ast import generate_functions
from vypa_compiler.internals._codegen import CodeGenerator

__author__ = "Adam Múdry and Daniel Paul"
__copyright__ = "Copyright 2022, VYPa Compiler Project 2022"
__credits__ = ["Adam Múdry", "Daniel Paul"]

__license__ = "MIT"
__version__ = "0.0.1"

DEBUG = True

def compile(source_string: str) -> str:
    """Compiles the source string and returns the result"""
    symbol_table.clear()
    
    lexer = make_lexer()
    parser = make_parser()
    parsed = parser.parse(source_string)
    symbol_table.append(Scope()) # global scope
    add_built_in_functions_to_symtable()
    program = Program(parsed)
    asts = generate_functions(symbol_table)
    generator = CodeGenerator(asts)
    generator.generate()
    return str(generator)

def main():
    SOURCE_FILE = ""
    OUTPUT_FILE = "out.vc"

    args = sys.argv[1:]
    if (argc := len(args)) == 1:
        SOURCE_FILE = args[0]
    elif argc == 2:
        SOURCE_FILE = args[0]
        OUTPUT_FILE = args[1]
    else:
        eprint("Error: Invalid number of arguments")
        exit(ExitCode.ERR_INTERNAL)

    
    input_data: str
    try:
        with open(SOURCE_FILE, encoding='utf-8') as f:
            input_data = f.read()
    except Exception as e:
        eprint(f"Error: {e}")
        exit(ExitCode.ERR_INTERNAL)

    lexer = make_lexer()
    if DEBUG == True:
        print("Tokens:")
        lexer.input(input_data)
        while True:
            tok = lexer.token()
            if not tok: 
                break
            print(tok)
        print("")
    
    parser = make_parser()
    parsed = parser.parse(input_data, tracking=True)
    symbol_table.append(Scope()) # global scope
    add_built_in_functions_to_symtable()
    program = Program(parsed)
    asts = generate_functions(symbol_table)
    generator = CodeGenerator(asts)
    generator.generate()
    generator.print_code(OUTPUT_FILE)

if __name__ == "__main__":
    main()
