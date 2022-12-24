#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

import pytest

from vypa_compiler.compiler import compile
from vypa_compiler.internals._utils import ExitCode

src = [
  'void main( {}', # Missing closing parenthesis
  'void main() {}' # Missing void parameter
  'void main(void) }', # Missing opening brace
  'return;', # Return statement has to be in function
  'print(1, "haha")', # Function call has to be in function
]

src_ok = ["void main(void) {int a; a = 1; print(a); return;}"]

def test_syntax_error():
    for s in src:
      with pytest.raises(SystemExit) as e_info:
        compile(s)
      assert e_info.value.code is ExitCode.ERR_SYN

def test_syntax_ok():
    for s in src_ok:
        compile(s)