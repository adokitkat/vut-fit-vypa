#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

"""VYPa Compiler Project 2022

Main source file
"""

import os, sys

import ply.lex as lex
import pprint

#from vypa_compiler.internals._models import *
from vypa_compiler.internals._utils import eprint, ExitCode, sublist_lookup # ,convert_to_lists
from vypa_compiler.internals._lexer import make_lexer
from vypa_compiler.internals._parser import make_parser
from vypa_compiler.internals._models import symbol_table, add_built_in_functions_to_symtable, Program


__author__ = "Adam Múdry and Daniel Paul"
__copyright__ = "Copyright 2022, VYPa Compiler Project 2022"
__credits__ = ["Adam Múdry", "Daniel Paul"]

__license__ = "MIT"
__version__ = "0.0.1"

SOURCE_FILE = ""
OUTPUT_FILE = "out.vc"

DEBUG = True

def main():
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
    print("Simulation of derivation tree:")
    pprint.pprint(parsed)

    add_built_in_functions_to_symtable()
    #parsed_list = convert_to_lists(parsed)
    #pprint.pprint(parsed_list, indent=4)
    program = Program(parsed)
    #print(program)
    print(symbol_table)
    #print([x.symtable for x in program.classes])
    #print(list(symbol_table[0].scope.values())[0].symtable)

if __name__ == "__main__":
    main()
