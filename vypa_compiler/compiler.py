#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

"""VYPa Compiler Project 2022

Main source file
"""

import sys

import ply.lex as lex

from vypa_compiler.internals._utils import eprint, ExitCode
from vypa_compiler.internals._lexer import make_lexer
from vypa_compiler.internals._parser import make_parser

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
    parser.parse(input_data)

if __name__ == "__main__":
    main()