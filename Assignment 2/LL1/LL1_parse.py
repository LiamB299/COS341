from definitions2 import *
import tabulate
from parse_tree import *
from LL1_table import *
import re
from render_tree import *
import os
from output import write_to_xml

def peak(stack: []):
    if len(stack) == 0:
        raise Exception('Empty Stack')

    ret = stack.pop()
    stack.append(ret)

    return ret


def add_children(parent: NT_node, children):
    parent.add_children(children)


def match_symbol(symbol, match_table):
    match_table.append(symbol)


def make_nodes(RHS: str):
    nodes = []
    for symbol in RHS:
        if symbol in non_terminals:
            nodes.append(NT_node(symbol))
        elif symbol in terminals and not symbol == 'ε':
            nodes.append(T_node(symbol))
        elif symbol == 'ε':
            continue
        else:
            raise Exception('Symbol "' + symbol + '" unknown')

    return nodes


def split_and_reverse(string, word_list):
    # Create a regex pattern that matches any word in the word list
    pattern = '|'.join(map(re.escape, word_list))

    # Split the string based on the pattern, keeping the delimiters
    parts = re.split(f'({pattern})', string)

    # Remove any empty parts and return the result
    return [part for part in parts if part]


def validate_comments(expression):
    arr = []
    i = 0
    while not i == len(expression):
        if expression[i] in '"*':
            arr.append(expression[i])
            sub_expression = ''
            for j in range(i+1, len(expression)):
                if expression[j] in '*"':
                    if not len(sub_expression) == 15:
                        raise Exception('Comment / String too short')
                    else:
                        arr.append(sub_expression)
                        arr.append(expression[j])
                        i = j+1
                        break
                is_ascii(expression[j])
                sub_expression += expression[j]
        else:
            if not expression[i] == ' ':
                arr.append(expression[i])
            i += 1
    return arr


def is_ascii(sub):
    for item in sub:
        if not ord(item) < 128:
            raise Exception('Comment / String not Ascii')


def remove_whitespace(express):
    expression = ''
    comment = False
    for c in express:
        if c in '"*':
            comment = not comment
        if c == ' ' and not comment:
            continue
        else:
            expression += c
    return expression


def check_floats(expression):
    i = 0
    while not i == len(expression):
        symbol = expression[i]
        if symbol == '.':
            if i < 1:
                raise Exception('Bad floats')
            elif expression[i-2].isdigit() or not expression[i-1] == '0':
                i += 1
                continue
            else:
                f = ''
                for j in range(i-1, i+3):
                    f += expression[j]
                expression.pop(i - 1)
                expression.pop(i - 1)
                expression.pop(i - 1)
                expression.pop(i - 1)
                expression.insert(i-1, f)
                i -= 1
        i += 1
    return expression



def parse_LL1_grammar(express: str, parse_table):
    stack: [NT_node | T_node] = []
    node_table = []

    # push start non-terminal onto stack
    stack.append(NT_node(non_terminals[0]))
    expression = remove_whitespace(express)
    expression = split_expression(expression)
    expression = validate_comments(expression)
    expression = check_floats(expression)

    i = 0
    while not len(stack) == 0:
        if peak(stack).label in terminals:
            # match top
            match_symbol(peak(stack), node_table)
            stack.pop()
            i += 1
        elif (peak(stack).label, expression[i]) not in parse_table and not peak(stack).label == 'C':
            print(peak(stack).label, expression[i])
            raise Exception('Parse Error - No Transition')

        # non-terminal is found
        # get RHS of symbol
        else:
            if peak(stack).label == 'C':
                sequence = expression[i]
                while not sequence == '':
                    terminal_node = stack.pop()
                    node_table.append(terminal_node)
                    child = [T_node(sequence[0])]
                    add_children(terminal_node, child)
                    stack += child
                    sequence = sequence[1:]
                    match_symbol(peak(stack), node_table)
                    stack.pop()
                i += 1
            else:
                terminal_node = stack.pop()
                node_table.append(terminal_node)
                rhs = parse_table[terminal_node.label, expression[i]]
                rhs = split_and_reverse(rhs, non_terminals)
                rhs = rhs[::-1]
                children = make_nodes(rhs)
                add_children(terminal_node, children)
                stack += children

    return node_table[0]


def bfs_print(node: NT_node | T_node):
    ret = {}

    if not node.is_terminal:
        arr = []
        key_arr = []
        for child in node.children:
            key_arr.append(child.label)
            if child.is_terminal:
                arr.append([])
            else:
                arr.append(bfs_print(child))
        ret['keys'] = key_arr
        ret['children'] = arr
    else:
        ret['keys'] = [node.label]

    return ret


def traverse_tree(node, vertices: [], edges: []):
    if not node.is_terminal:
        vertices.append(node.label)
        if len(node.children) == 0:
            return edges.append([node.label, 'ε'])
        for child in node.children:
            edges.append([node.label, child.label])
        for child in node.children:
            traverse_tree(child, vertices, edges)
    else:
        vertices.append(node.label)


def split_expression(expression:str):
    arr = split_and_reverse(expression, terminals)
    return arr


def runner(expression= '', file=''):
    if expression == '':
        if file == '':
            file = input("Please input a filename or path with extension:\n")
            if not os.path.exists(file):
                print("No file found for path:\n"+file)
                return

        with open(file, 'r') as open_file:
            for line in open_file:
                expression += line.rstrip()

    print('Building parse table')
    parse_table = build_LL1_table()

    print('Parsing expression')
    try:
        match_table = parse_LL1_grammar(expression + '$', parse_table)
    except Exception as e:
        print(str(e))
        # e.with_traceback()
        return 0
    # print(match_table)

    print('Parse Complete')
    vertices = []
    edges = []
    traverse_tree(match_table, vertices, edges)
    render_graph(vertices, edges)
    write_to_xml(match_table)
    return


# runner("n26:=a(n36,n49)")
# runner('n2:=a(n3,n4);s5:="PROCDEFPROCDEF ";h')
# runner('n2:=a(n3,n4);s5:="PROCDEFPROCDEF ";h;i(T)t{h}e{h}')
runner('', 'test_cases/t7')