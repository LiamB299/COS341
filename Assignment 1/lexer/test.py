import re


def epsilon_nfa(regex):
    """
    Convert a regular expression to an epsilon NFA using dictionaries.
    """
    nfa = {}
    stack = [0]
    state = 1

    for char in regex:
        if char == '(':
            stack.append(state)
        elif char == '|':
            state += 1
            nfa[state] = {}
            nfa[state][stack.pop()] = ''
            nfa[state][state + 1] = ''
            stack.append(state)
        elif char == ')':
            state += 1
            nfa[state] = {}
            nfa[state][stack.pop()] = ''
            nfa[stack.pop()][state] = ''
            stack.append(state)
        elif char == '*':
            nfa[stack[-1]][stack[-1]] = ''
        elif char == '+':
            state += 1
            nfa[state] = {}
            nfa[state][stack.pop()] = ''
            nfa[stack[-1]][state] = ''
            stack.append(state)
        elif char == '?':
            state += 1
            nfa[state] = {}
            nfa[state][stack.pop()] = ''
            nfa[stack[-1]][state] = ''
            nfa[state + 1] = {}
            nfa[state][state + 1] = ''
            stack.append(state)
        else:
            state += 1
            nfa[state] = {}
            nfa[state - 1][state] = char
            stack.append(state)

    nfa['start'] = {0: ''}
    nfa[stack.pop()] = {'end': ''}

    return nfa

print(epsilon_nfa("a|b"))