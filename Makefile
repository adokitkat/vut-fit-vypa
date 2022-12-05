# Project name: Compiler Implementation for VYPlanguage Programming Language
# Authors: Adam Múdry (xmudry01), Daniel Paul (xpauld00)

init:
	python3 -m pip install -r requirements.txt
	python3 setup.py install --user

test:
	python3 -m pytest tests

clean:
	find -type d -name '__pycache__' | xargs rm -rf
	rm -rf .pytest_cache build dist VYPa_Compiler_Project_2022.egg-info

all: init

.PHONY: init test run clean all