non_terminals = [
    "X",
    "EXP",
    "TWO",
    "THREE",
    "R"
]

terminals = [
    '*',
    '+',
    '-',
    '/',
    ')',
    '(',
    'n'
]

# TOP RULE IS THE START SYMBOL
rules = [
    "X ::= EXP",
    "EXP ::= EXP+TWO",
    "EXP ::= EXP-TWO",
    "EXP ::= TWO",
    "TWO ::= TWO*THREE",
    "TWO ::= TWO/THREE",
    "TWO ::= THREE",
    "THREE ::= n",
    "THREE ::= (EXP)"
]
