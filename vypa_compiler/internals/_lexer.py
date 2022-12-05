#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

from ply.lex import lex

"""VYPa Compiler Project 2022

Lexer implementation
"""

tokens = (
    'VARIABLE', 'NUMBER',
)

literals = ['=', '+', '-', '*', '/', '(', ')']

# TODO

vypa_lexer = lex