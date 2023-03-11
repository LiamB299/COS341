from parser import parser, _nfa_block


def generate_powerset(nfa: _nfa_block):
    # get number of states
    n_states = len(nfa['states'])

    # normal set
    normal_set = []

    # generate set
    for i in range(1, n_states + 1):
        normal_set.append(i)

    # generate powerset
    # credit: https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    powerset = []
    x = len(normal_set)
    for i in range(1 << x):
        powerset.append([normal_set[j] for j in range(x) if (i & (1 << j))])

    return powerset


def generate_basic_closures(nfa: _nfa_block):
    # get number of states
    n_states = len(nfa['states'])

    states_closures = []
    for i in range(1, n_states+1):
        current_closure = []
        visit_state(nfa, i, current_closure)
        states_closures.append({'state':i, 'closure': current_closure})

    return states_closures


def visit_state(nfa: _nfa_block, current_state: int, visited : []):
    # this state is visited
    visited.append(current_state)

    # get current state
    for state in nfa['states']:
        if state['state'] == current_state:
            break

    # if state has epsilon transition go to it
    for i, input_char in enumerate(state['input']):
        if input_char == '#' and state['next_state'][i] == -1:
            continue
        if input_char == "#":
            if state['next_state'][i] not in visited:
                visit_state(nfa, state['next_state'][i], visited)


nfa = parser("a|b", "a|b")
print(generate_basic_closures(nfa))
