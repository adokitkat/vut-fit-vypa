# VYPa 2022

Simplified project structure:

```text
├── doc                        Documentation files
│   └── ...
├── tests                      Test files
│   └── ...
├── vypa_compiler              Compiler source files
│   ├── generated
│   │   └── ...
│   ├── internals
│   │   ├── _ast.py            Abstract syntax tree implementation
│   │   ├── _code_templates.py Instruction templates
│   │   ├── _codegen.py        Code generation implementation
│   │   ├── _instructions.py   Target instructions
│   │   ├── _lexer.py          Lexer implementation
│   │   ├── _model.py          Symbol table, semantics, etc.
│   │   ├── _parser.py         Parser implementation
│   │   └── _utils.py          Utility functions
│   └── compiler.py            Main source file
│
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
- [x] Syntax analysis
- [ ] Semantic analysis
- [x] Construct AST
- [x] Target code generation (partially)

### Features / Other

- [x] Symbol table, variables
- [x] Operator precedence
- [x] If-Else
- [X] While
- [x] Functions
- [X] Built-in Functions
  - [x] Print
  - [X] Cast INT STRING 
  - ...
- [ ] OOP
  - [ ] Classes, objects
  - [ ] Inheritance
   
Etc.
