non_terminals = [
    "START",
    "PROGR",
    "PROCDEFS",
    "PROC",
    "DIGITS",
    "D",
    "MORE",
    "ALGO",
    "SEQ",
    "INSTR",
    "CALL",
    "ASSIGN",
    "LOOP",
    "BRANCH",
    "ELSE",
    "NUMVAR",
    "BOOLVAR",
    "STRINGV",
    "NUMEXPR",
    "DECNUM",
    "NEG",
    "POS",
    "INT",
    "BOOLEXPR",
    "LOGIC",
    "CMPR",
    "STRI",
    "C",
    "KOMMENT",
    "INPUT",
    "OUTPUT",
    "VALUE",
    "TEXT"
]

terminals = [
    ',',
    'p',
    '{',
    '}',
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    ';',
    'h',
    'c',
    'cp',
    ':',
    ':=',
    'w',
    '(',
    ')',
    'i',
    't',
    'e',
    'n',
    'b',
    's',
    'a',
    'm',
    'd',
    '.',
    '-',
    'T',
    'F',
    '^',
    'v',
    '!',
    'E',
    '<',
    '>',
    '"',
    '*',
    'g',
    'o',
    'r'
]

# TOP RULE IS THE START SYMBOL
rules = [
    "START ::= PROGR",
    "PROGR ::= ALGO PROCDEFS",
    "PROCDEFS ::= , PROC PROCDEFS",
    "PROCDEFS ::= ε",
    "PROC ::= p DIGITS { PROGR }",
    "DIGITS ::= D MORE",
    #"D ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9",
    "D ::= 0",
    "D ::= 1",
    "D ::= 2",
    "D ::= 3",
    "D ::= 4",
    "D ::= 5",
    "D ::= 6",
    "D ::= 7",
    "D ::= 8",
    "D ::= 9",
    "MORE ::= DIGITS",
    "MORE ::= ε",
    "ALGO ::= INSTR KOMMENT SEQ",
    "SEQ ::= ; ALGO",
    "SEQ ::= ε",
    "INSTR ::= INPUT",
    "INSTR ::= OUTPUT",
    "INSTR ::= ASSIGN",
    "INSTR ::= CALL",
    "INSTR ::= LOOP",
    "INSTR ::= BRANCH",
    "INSTR ::= h",
    "CALL ::= c pDIGITS",
    "ASSIGN ::= NUMVAR := NUMEXPR",
    "ASSIGN ::= BOOLVAR := BOOLEXPR",
    "ASSIGN ::= STRINGV := STRI",
    "LOOP ::= w ( BOOLEXPR ) { ALGO }",
    "BRANCH ::= i ( BOOLEXPR ) t { ALGO } ELSE",
    "ELSE ::= e { ALGO }",
    "ELSE ::= ε",
    "NUMVAR ::= n DIGITS",
    "BOOLVAR ::= b DIGITS",
    "STRINGV ::= s DIGITS",
    "NUMEXPR ::= a ( NUMEXPR , NUMEXPR )",
    "NUMEXPR ::= m ( NUMEXPR , NUMEXPR )",
    "NUMEXPR ::= d ( NUMEXPR , NUMEXPR )",
    "NUMEXPR ::= NUMVAR",
    "NUMEXPR ::= DECNUM",
    # "DECNUM ::= 0.00 | NEG | POS",
    "DECNUM ::= 0.00",
    "DECNUM ::= NEG",
    "DECNUM ::= POS",
    "NEG ::= ‒POS",
    "POS ::= INT.DD",
    #"INT ::= 1MORE | 2MORE | 3MORE | 4MORE | 5MORE | 6MORE | 7MORE | 8MORE | 9MORE",
    "INT ::= 1MORE",
    "INT ::= 2MORE",
    "INT ::= 3MORE",
    "INT ::= 4MORE",
    "INT ::= 5MORE",
    "INT ::= 6MORE",
    "INT ::= 7MORE",
    "INT ::= 8MORE",
    "INT ::= 9MORE",
    "BOOLEXPR ::= LOGIC",
    "BOOLEXPR ::= CMPR",
    "LOGIC ::= BOOLVAR",
    # "LOGIC ::= T | F",
    "LOGIC ::= T",
    "LOGIC ::= F",
    "LOGIC ::= ^ ( BOOLEXPR , BOOLEXPR )",
    "LOGIC ::= v ( BOOLEXPR , BOOLEXPR )",
    "LOGIC ::= ! ( BOOLEXPR )",
    "CMPR ::= E ( NUMEXPR , NUMEXPR )",
    "CMPR ::= < ( NUMEXPR , NUMEXPR )",
    "CMPR ::= > ( NUMEXPR , NUMEXPR )",
    "STRI ::= \"C C C C C C C C C C C C C C C\"",
    "C ::= (ascii)",
    "KOMMENT ::= *C C C C C C C C C C C C C C C*",
    "KOMMENT ::= ε",
    "INPUT ::= g NUMVAR",
    # "OUTPUT ::= TEXT | VALUE",
    "OUTPUT ::= TEXT",
    "OUTPUT ::= VALUE",
    "VALUE ::= o NUMVAR",
    "TEXT ::= r STRINGV"
]
