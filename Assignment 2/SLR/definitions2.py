non_terminals = [
    "T'",
    "T",
    "R"
]

follow = [
    [],
    ['$', 'c'],
    ['$', 'c']
]

terminals = [
    '$',
    'a',
    'b',
    'c'
]

# TOP RULE IS THE START SYMBOL
rules = [
    "T' ::= T$",
    "T ::= R",
    "T ::= aTc",
    "R ::= ε",
    "R ::= bR",
]

first = [
    ['g', 'r', 'o', 'n', 'b', 's', 'c', 'w', 'i', 'h'],
    ['g', 'r', 'o', 'n', 'b', 's', 'c', 'w', 'i', 'h'],
    [','],
    ['ε'],
    ['p'],
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    ['ε'],
    ['g', 'r', 'o', 'n', 'b', 's', 'c', 'w', 'i', 'h'],
    [';'],
    ['ε'],
    ['g'],
    ['r', 'o'],
    ['n', 'b', 's'],
    ['c'],
    ['w'],
    ['i'],
    ['h'],
    ['c'],
    ['n'],
    ['b'],
    ['s'],
    ['w'],
    ['i'],
    ['e'],
    ['ε'],
    ['n'],
    ['b'],
    ['s'],
    ['a'],
    ['m'],
    ['d'],
    ['n'],
    ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    ['0'],
    ['-'],
    ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    ['-'],
    ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    ['1'],
    ['2'],
    ['3'],
    ['4'],
    ['5'],
    ['6'],
    ['7'],
    ['8'],
    ['9'],
    ['b', 'T', 'F', '^', 'v', '!'],
    ['E', '<', '>'],
    ['b'],
    ['T'],
    ['F'],
    ['^'],
    ['v'],
    ['!'],
    ['E'],
    ['<'],
    ['>'],
    ['"'],
    ['ASCII'],
    ['*'],
    ['ε'],
    ['g'],
    ['r'],
    ['o'],
    ['o'],
    ['r'],
]

nullable = [
    False,
    False,
    False,
    True,
    False,
    False,
    False,
    True,
    False,
    False,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    True,
    False,
    False,
    False,
    False,
    False,
]