#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

import sys
from enum import IntEnum

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Performs lookup in derivation tree
def sublist_lookup(lst, target):
    result = []
    found = False
    for item in lst:
        if found == True:
            result.append(item)
            found = False
        if isinstance(item, (list, tuple)):
            result.extend(sublist_lookup(item, target))
        elif item == target:
            found = True
    return result

class ExitCode(IntEnum):
    ERR_LEX = 11
    ERR_SYN = 12
    ERR_SEM_TYPE_INCOMP = 13
    ERR_SEM_REST = 14
    ERR_TARGET_CODE_GEN = 15
    ERR_INTERNAL = 19
