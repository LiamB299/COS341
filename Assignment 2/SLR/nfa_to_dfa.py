from classes import NfaState, NfaBlock, Transition, tabulate
import itertools


def print_table1(table):
    array = []
    for key, value in table.items():
        try:
            array.append([key, value.transition_input, value.to_state.state_label])
        except:
            array.append([key, value.transition_input, value.to_state])

    # Print the table
    print(tabulate(array, headers=["State", "Input", "Next"]))


def print_table2(table):
    array = []
    for key, value in table.items():
        try:
            for val in value['to_state']:
                array.append([key, value['input'], val])
        except:
            array.append([key, value['input'], ""])
    # Print the table
    print(tabulate(array, headers=["State", "Input", "Next"], tablefmt='None'))


def df_search(current: NfaState, visited: []):
    visited.append(current.state_label)
    for state in current.epsilon_transitions:
        if state.state_label not in visited:
            df_search(state, visited)


def generate_transition_table(nfa: [NfaBlock]):
    # get base transitions table
    transitions = {}
    for block in nfa:
        current = block.start_symbol
        while not current == 0:
            transitions[current.state_label] = Transition(current.symbol_transition, current.next, current.terminal_transition)
            current = current.next
    # print_table1(transitions)
    return transitions


def generate_transition_closures(transition_table: {}):
    base_new_transition_table = {}
    for key, transition_info in transition_table.items():
        visited = []
        if not transition_info.to_state == 0:
            df_search(transition_info.to_state, visited)
            base_new_transition_table[key] = {"input": transition_info.transition_input,
                                              "to_state": set(visited)}
        else:
            base_new_transition_table[key] = {"input": transition_info.transition_input,
                                              "to_state": []}

    # print_table2(base_new_transition_table)
    return base_new_transition_table


def generate_basic_closures(nfa_states: [NfaState]):
    closures = {}
    for state in nfa_states:
        visited = []
        df_search(state, visited)
        closures[state.state_label] = visited
    return closures


def generate_powerset(state_list):
    keys = set(state_list)

    powerset = []
    for i in range(len(keys) + 1):
        powerset += itertools.combinations(keys, i)

    pset = [set(list(item)) for item in powerset]
    # print(pset)
    return pset


def get_finishing_states(rule_block: [NfaBlock]):
    finishing_states = set([])
    for block in rule_block:
        for state in block.finishing_states:
            finishing_states.add(state)
    return finishing_states