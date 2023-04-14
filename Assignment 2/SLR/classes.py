from tabulate import tabulate
from definitions2 import *

class NfaState:
    terminal_transition = False
    finishing = False
    start = False
    finishing_number = -1
    next = 0
    prev = 0

    def __init__(self, symbol, label="", terminal=False):
        self.symbol_transition = symbol
        self.state_label = label
        self.terminal_transition = terminal
        self.epsilon_transitions = []

    def print_data(self):
        try:
            lnext = self.next.state_label

        except:
            lnext = 'none'

        finally:
            return [
                self.state_label,
                self.symbol_transition,
                self.terminal_transition,
                self.start,
                self.finishing,
                lnext
            ]

    def print_epsilons(self):
        data = []
        for state in self.epsilon_transitions:
            data.append([self.state_label, state.state_label])
        return data


class NfaBlock:
    expression = ""
    LHS_symbol = ""
    finishing_states = set([])
    start_symbol: NfaState = 0
    count = 0
    state_list = []

    def append_symbol(self, symbol: NfaState):
        self.state_list.append(symbol)
        if symbol.finishing:
            self.finishing_states.add(symbol.state_label)

        if not self.start_symbol:
            self.start_symbol = symbol
            symbol.start = True
            self.count = 1
            return

        current = self.start_symbol

        # go to end of dfa
        while current.next:
            current = current.next

        current.next = symbol
        symbol.prev = current
        self.count += 1

    def print_block(self):
        current: NfaState = self.start_symbol

        data = []
        epsilons = []
        # go to end of dfa
        while current:
            data.append(current.print_data())
            epsilons += current.print_epsilons()
            current = current.next

        headers = ["Label", "Transition Input", "Terminal Transition", "Start", "Finishing", "Next"]
        headers2 = ["This state", "epsilon transitions to"]

        # Generate the table
        table = tabulate(data, headers=headers, tablefmt="pipe")
        table2 = tabulate(epsilons, headers=headers2, tablefmt="pipe")

        # Print the table
        print(self.expression)
        print(table)
        print('\n')

        print("Epsilons")
        print(table2)
        print('\n')


class Transition:
    def __init__(self, _input, next, is_terminal):
        self.transition_input = _input
        self.to_state = next
        self.terminal = is_terminal


class DfaState:
    finishing = False
    starting = False
    prev = []
    state_label = ''

    def __init__(self):
        self.transitions = []
        self.containing_labels = set()

    def print_state(self):
        ret = []
        for transition in self.transitions:
            ret.append([
                self.state_label,
                self.containing_labels.__str__(),
                self.starting,
                self.finishing,
                transition.transition_input,
                transition.to_state.state_label
            ])
        if not len(ret):
            ret.append([
                self.state_label,
                self.containing_labels.__str__(),
                self.starting,
                self.finishing,
                "",
                ""
            ])
        return ret


class Dfa:
    start = 0

    def __init__(self):
        self.states = {}

    def add_state(self, state: DfaState):
        if self.start == 0:
            self.start = state
            self.start.starting = True
        self.states[state.state_label] = state

    # def find_state(self, containing_labels: set()):
    #     for key, state in self.states.items():
    #         if state.containing_labels == containing_labels:
    #             return state.state_label
    #     return 'D0'

    def add_transitions(self, transition_list):
        for state, t_list in transition_list.items():
            transitions = []
            for t_input, transition in t_list.items():
                transitions.append(Transition(t_input, self.states[transition], t_input in terminals))
                self.states[transition].prev = state
            self.states[state].transitions = transitions


    def get_state(self, state_label):
        try:
            return self.states[state_label]
        except:
            return self.states[0]

    def print_DFA(self):
        data = []
        for key, state in self.states.items():
            data += (state.print_state())

        headers = ["Label", "containing states", "Start", "Finishing", "Transition Input", "Next"]
        table = tabulate(data, headers=headers, tablefmt="pipe", missingval="?")

        with open('file.txt', 'w+') as file:
            file.write(table)
        print(table)
        print('\n')


class ParseAction:
    def __init__(self, _type, nfa_block):
        self.type = _type
        self.number = nfa_block

    def print_entry(self):
        return self.type + ' ' + self.number


class ParseTable:
    def __init__(self, size: int):
        self.table = {}
        for i in range(0, size):
            self.table[i] = {}

    def add_element(self, action: ParseAction, dfa_state: int, symbol: str):
        try:
            if self.table.get(dfa_state).get(symbol) is not None:
                raise Exception('Index:  ' + symbol + ',  ' + str(dfa_state) +
                                ' already exists with item:  ' + self.table[symbol][dfa_state].type)
            else:
                self.table[dfa_state][symbol] = []
        except Exception:
            print(Exception.with_traceback())
        finally:
            self.table[dfa_state][symbol].append(action)

    def get_element(self, dfa_state: int, symbol: str):
        try:
            return self.table[dfa_state][symbol]
        except KeyError:
            return ParseAction('none', -1)

    def print_table(self):
        data = []
        header = []
        for x_key, y_col in self.table.items():
            for y_key, action in y_col.items():
                header.apppend(y_key)

        for x_key, y_col in self.table.items():
            row = ["" for i in range(0, len(header) + 1)]
            for y_key, action in y_col.items():
                for i, item in enumerate(header):
                    if item == y_key:
                        row[i + 1] = item.print_entry
            row[0] = y_key
            data.append(row)

        table = tabulate.tabulate(data, header)
        print(table)
        print('\n')