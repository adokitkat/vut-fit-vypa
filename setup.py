#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

from setuptools import setup, find_packages

from vypa_compiler import compiler

# TODO: Do we even need this?
setup(
    name='VYPa Compiler Project 2022',
    version=compiler.__version__,
    author=compiler.__author__,
    url='https://github.com/adokitkat/vut-fit-vypa',
    packages=find_packages(),
    python_requires='>=3.8, <4',
)