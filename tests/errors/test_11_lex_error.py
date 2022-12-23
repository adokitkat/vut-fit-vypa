#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

import pytest

from vypa_compiler.compiler import compile
from vypa_compiler.internals._utils import ExitCode

src = [
  "[", "]" # Brackets are not allowed in source code
]

def test_lex_error():
    for s in src:
      with pytest.raises(SystemExit) as e_info:
        compile(s)
      assert e_info.value.code is ExitCode.ERR_LEX