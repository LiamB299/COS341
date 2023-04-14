import re
from definitions2 import non_terminals, terminals, rules
from classes import *
import uuid
from nfa_to_dfa import *


def generate_label_name(prefix):
    return prefix
    # unique_id = str(uuid.uuid4()).replace('-', '')  # Generate a random UUID and remove the dashes
    # return f"{prefix}_{unique_id}"


def split_string(string, word_list):
    # Create a regex pattern that matches any word in the word list
    pattern = '|'.join(map(re.escape, word_list))

    # Split the string based on the pattern, keeping the delimiters
    parts = re.split(f'({pattern})', string)

    # Remove any empty parts and return the result
    return [part for part in parts if part]


def parse_rule(rule: str, block_number: int):
    prod_symbol, production = rule.replace(" ", "").split("::=")
    products = split_string(production, non_terminals)
    nfa_block = NfaBlock()
    nfa_block.expression = rule

    # prod symbol for epsilon transitions
    nfa_block.LHS_symbol = prod_symbol

    # generate base NFA blocks
    if products[0] == 'ε':
        final_state = NfaState("##", generate_label_name("S" + str(block_number) + "0"), False)
        final_state.finishing_number = block_number
        final_state.finishing = True
        nfa_block.append_symbol(final_state)

    elif prod_symbol == 'C':
        state = NfaState("<ASCII>", generate_label_name("S" + str(block_number) + "0"), False)
        state.finishing_number = block_number
        nfa_block.append_symbol(state)
        final_state = NfaState("##", generate_label_name("S" + str(block_number) + "1"), False)
        final_state.finishing_number = block_number
        final_state.finishing = True
        nfa_block.append_symbol(final_state)

    else:
        for i, product in enumerate(products):
            state = NfaState(product, generate_label_name("S" + str(block_number) + str(i)),
                             product not in non_terminals)
            state.finishing_number = block_number
            nfa_block.append_symbol(state)
        final_state = NfaState("##", generate_label_name("S" + str(block_number) + str(i + 1)), False)
        final_state.finishing = True
        final_state.finishing_number = block_number
        nfa_block.append_symbol(final_state)

    return nfa_block


def generate_rule_blocks():
    nfa_blocks: [NfaBlock] = []
    for i, rule in enumerate(rules):
        nfa_blocks.append(parse_rule(rule, i))

    return nfa_blocks


def link_epsilons(nfa_blocks: [NfaBlock]):
    for block in nfa_blocks:
        # find RHS symbol
        current_symbol = block.start_symbol
        if current_symbol.start and not current_symbol.state_label == 'S00':
            current_symbol.start = False
        while current_symbol != 0:
            if not current_symbol.terminal_transition:
                # compare to LHS Prods to find links
                for compare_block in nfa_blocks:
                    if compare_block.LHS_symbol == current_symbol.symbol_transition:
                        current_symbol.epsilon_transitions.append(compare_block.start_symbol)
            current_symbol = current_symbol.next


def print_new_trans(transitions):
    data = []
    for key, item_transitions in transitions.items():
        for sub_key, sub_transitions in item_transitions.items():
            data += [
                key,
                sub_key,
                sub_transitions
            ]

    headers = ["State", "Input", "Transition"]
    table = tabulate(data, headers=headers, tablefmt="pipe")
    print(table)
    print('\n')


def generate_base_dfa(dfa, powerset, finishing_states):
    for i, pset in enumerate(powerset):
        state = DfaState()
        state.state_label = 'D' + str(i)
        state.containing_labels = pset
        if len(finishing_states.intersection(pset)) > 0:
            state.finishing = True

        dfa.add_state(state)
    return 0


def build_closure_transitions(powerset, basic_closures):
    transitions = []
    for pset in powerset:
        transition = {}
        for base_set, base_transition in basic_closures.items():
            if base_set in pset:
                if base_transition['input'] in transition:
                    transition[base_transition['input']].union(base_transition['to_state'])
                else:
                    transition[base_transition['input']] = base_transition['to_state']
        transitions.append({'state': pset, "transitions": transition})
    return transitions


def link_dfa(dfa, closure_transitions):
    for closure_transition in closure_transitions:
        current_state = dfa.find_state(closure_transition['state'])
        transitions = []
        for input_symbol, to_state in closure_transition['transitions'].items():
            ref_to_state = dfa.get_state(dfa.find_state(to_state))
            transitions.append(Transition(input_symbol, ref_to_state, input_symbol in terminals))
        dfa.add_transitions(current_state, transitions)
    dfa.print_DFA()


# def add_state(state_number:int, containing_labels:list(str), )


def build_dfa(nfa: [NfaBlock], closures, transition_table, closure_transitions, finishing_states):
    dfa_transitions = {}
    unstr_states = []
    # state_count = 1
    start = nfa[0].start_symbol
    state = DfaState()
    # state.state_label = 'D'+str(state_count)

    # generate new start state from closure of start state
    start_closure = closures[start.state_label]
    unstr_states.append(start_closure)
    state.containing_labels = set(start_closure)
    state.state_label = start_closure.__str__()

    # generate transitions

    # loop through containing labels / states and add their transition closures as transitions
    transitions = {}
    for sub_state in state.containing_labels:
        closure_transition = closure_transitions[sub_state]
        if closure_transition['input'] == '##':
            continue
        if closure_transition['input'] in transitions:
            transitions[closure_transition['input']] = transitions[closure_transition['input']].union(closure_transition['to_state'])
        else:
            transitions[closure_transition['input']] = closure_transition['to_state']

    # add to states as states to be generated
    build_stack = []
    for symbol_input, t_state in transitions.items():
        build_stack.append(t_state)

    # add state to add list
    dfa_transitions[state.state_label] = transitions

    while len(build_stack):
        state_set = build_stack.pop()
        if state_set.__str__() in dfa_transitions:
            continue

        unstr_states.append(state_set)

        state = DfaState()

        state.state_label = state_set
        state.containing_labels = state_set

        # generate transitions

        # loop through containing labels / states and add their transition closures as transitions
        transitions = {}
        for sub_state in state.containing_labels:
            closure_transition = closure_transitions[sub_state]
            if closure_transition['input'] == '##':
                continue
            if closure_transition['input'] in transitions:
                transitions[closure_transition['input']].union(closure_transition['to_state'])
            else:
                transitions[closure_transition['input']] = closure_transition['to_state']

        # add to states as states to be generated
        for symbol_input, t_state in transitions.items():
            build_stack.append(t_state)

        # add state to add list
        dfa_transitions[state.state_label.__str__()] = transitions

    # build dfa
    count = 1
    dfa_states = []
    for state in unstr_states:
        dfa_states.append(DfaState())
        dfa_states[count - 1].state_label = 'D' + str(count)
        dfa_states[count - 1].containing_labels = state
        count += 1

    labelled_transitions = {}
    for current_state in dfa_states:
        for _state, transitions in dfa_transitions.items():
            for _input, compare_state in transitions.items():
                if compare_state == current_state.containing_labels:
                    transitions[_input] = current_state.state_label

    for state, transitions in dfa_transitions.items():
        for dfa_state in dfa_states:
            if dfa_state.containing_labels.__str__() == state:
                labelled_transitions[dfa_state.state_label] = transitions

    dfa = Dfa()
    for state in dfa_states:
        if not finishing_states.isdisjoint(state.containing_labels):
            state.finishing = True
        dfa.add_state(state)

    dfa.add_transitions(labelled_transitions)

    return dfa


def generate_dfa():
    # generate base NFAs
    rule_blocks = generate_rule_blocks()

    for block in rule_blocks:
        block.print_block()

    # generate epsilons
    link_epsilons(rule_blocks)

    # make transition table
    trans_table = generate_transition_table(rule_blocks)

    # using transition table, make base closures
    base_closures = generate_basic_closures(rule_blocks[0].state_list)

    # make base closure transition table
    closure_transitions = generate_transition_closures(trans_table)

    # get finishing states
    finishing_states = get_finishing_states(rule_blocks)

    # build dfa from starting state
    dfa = build_dfa(rule_blocks, base_closures, trans_table, closure_transitions, finishing_states)

    #dfa.print_DFA()

    return dfa, rule_blocks
