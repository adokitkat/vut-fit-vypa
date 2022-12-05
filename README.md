# VYPa 2022

Simplified project structure:

```text
├── doc                        Documentation files
│   └── ...
├── tests                      Test files
│   └── ...
├── vypa_compiler              Compiler source files
│   ├── compiler.py            Main source file
│   └── internals
│       ├── _utils.py          Utility functions
│       ├── _lexer.py          Lexer implementation
│       └── _parser.py         Parser implementation
├── .gitignore
├── LICENSE
├── Makefile                   Makefile script
├── README.md
├── requirements.txt           Pip dependencies
├── setup.py                   Setup script 
└── vypcomp                    Complier executable
```

## Getting started

### Setup

Initialize the project before running:

`make`

### Running the compiler

`vypcomp SOURCE_FILE [OUTPUT_FILE]`

Default output file name is `out.vc`.

## Progress

### Compiler stages

- [x] Lexical analysis
  - Source code lexemes to tokens
- [ ] Syntax analysis
- [ ] Semantic analysis
  - Construct AST
- [ ] Target code generation

### Features / Other

- [ ] Symbol table, variables
- [ ] Operator precedence
- [ ] Functions
- [ ] OOP
  - [ ] Classes, objects
  - [ ] Inheritance

Etc.
