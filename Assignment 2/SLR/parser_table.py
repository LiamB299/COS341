import tabulate
from classes import *
from definitions2 import *
from nfa_generator import *


def go_actions(parse_table: ParseTable, dfa: Dfa, nfa: [NfaBlock]):
    # iterate through transitions for Non-terminals
    for state_name, state in dfa.states.items():
        # get nfa first nfa block transitions refers to
        for transition in state.transitions:
            if not transition.terminal:
                state: NfaState
                for i, nfa_state in enumerate(nfa[0].state_list):
                    if nfa_state.symbol_transition == transition.transition_input:
                        parse_table.add_element(ParseAction('g' + nfa_state.state_label[1:],
                                                            i),
                                                int(state_name[1:])-1, nfa_state.symbol_transition)
                        break


def shift_actions(parse_table: ParseTable, dfa: Dfa, nfa: [NfaBlock]):
    # iterate through transitions for Non-terminals
    for state_name, state in dfa.states.items():
        # get nfa first nfa block transitions refers to
        for transition in state:
            if transition.terminal:
                state: NfaState
                for state in nfa[0].state_list:
                    if state.symbol_transition == transition.transition_input:
                        parse_table.add_element(ParseAction('s' + state.state_label[1:],
                                                            state_name[1:], state.symbol_transition))
                        break


def generate_parse_table():
    dfa, nfa = generate_dfa()

    parse_table = ParseTable(len(dfa.states))

    go_actions(parse_table, dfa, nfa)

    return parse_table


generate_parse_table()
