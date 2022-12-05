# VYPa 2022

Simplified project structure:

```text
├── vypa_compiler              Project folder
│   ├── compiler.py            Main source file
│   └── internals
│       ├── _utils.py          Utility functions
│       ├── _lexer.py          Lexer implementation
│       └── _parser.py         Parser implementation
├── tests
│   └── ...                    Test files
├── Makefile
├── README.md
├── requirements.txt           Pip dependencies
└── setup.py                   Setup file 
```

## Getting started

### Setup

Initialize the project before running:

`make`

### Running the compiler

`vypcomp SOURCE_FILE [OUTPUT_FILE]`

Default output file name is `out.vc`.
