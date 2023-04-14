from definitions2 import *
import tabulate
from parse_tree import *
from LL1_table import *
import re
from render_tree import *


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
            raise Exception('Symbol ' + symbol + ' unknown')

    return nodes


def split_and_reverse(string, word_list):
    # Create a regex pattern that matches any word in the word list
    pattern = '|'.join(map(re.escape, word_list))

    # Split the string based on the pattern, keeping the delimiters
    parts = re.split(f'({pattern})', string)

    # Remove any empty parts and return the result
    return [part for part in parts if part]


def parse_LL1_grammar(expression: str, parse_table):
    stack: [NT_node | T_node] = []
    node_table = []

    # push start non-terminal onto stack
    stack.append(NT_node(non_terminals[0]))

    i = 0
    while not len(stack) == 0:
        if peak(stack).label in terminals:
            # match top
            match_symbol(peak(stack), node_table)
            stack.pop()
            i += 1

        elif (peak(stack).label, expression[i]) not in parse_table:
            raise Exception('Parse Error')

        # non-terminal is found
        # get RHS of symbol
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

    if node.is_terminal == False:
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


def runner(expression: str):
    parse_table = build_LL1_table()
    match_table = parse_LL1_grammar(expression + '$', parse_table)
    # print(match_table)
    vertices = []
    edges = []
    traverse_tree(match_table, vertices, edges)
    return render_graph(vertices, edges)


runner("gn123")
