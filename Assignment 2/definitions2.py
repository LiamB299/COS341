non_terminals = [
    "T'",
    "T",
    "R"
]

terminals = [
    'a',
    'b',
    'c'
]

# TOP RULE IS THE START SYMBOL
rules = [
    "T' ::= T",
    "T ::= R",
    "T ::= aTc",
    "R ::= ε",
    "R ::= bR",
]
