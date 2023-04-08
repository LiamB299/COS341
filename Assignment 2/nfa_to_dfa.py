from classes import NfaState, NfaBlock, Transition, tabulate


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
            transitions[current.state_label] = Transition(current.symbol_transition, current.next)
            current = current.next
    return transitions


def generate_basic_closures(transition_table: {}):
    base_new_transition_table = {}
    for key, transition_info in transition_table.items():
        visited = [key]
        if not transition_info.to_state == 0:
            df_search(transition_info.to_state, visited)
            base_new_transition_table[key] = {"input": transition_info.transition_input,
                                              "to_state": visited}
        else:
            base_new_transition_table[key] = {"input": transition_info.transition_input,
                                              "to_state": []}

# def generate_powerset()

    print_table2(base_new_transition_table)
