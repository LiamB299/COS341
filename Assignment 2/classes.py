from tabulate import tabulate


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
    def __init__(self, _input, next):
        self.transition_input = _input
        self.to_state = next


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
                self.containing_labels,
                self.starting,
                self.finishing,
                transition.transition_input,
                transition.to_state.state_label
            ])
        return ret


class Dfa:
    start = 0
    reverse_list = {}

    def __init__(self):
        self.states = {}

    def add_state(self, state: DfaState):
        if self.start == 0:
            self.start = state
            self.start.starting = True
        self.states[state.state_label] = state

    def find_state(self, containing_labels: set()):
        for key, state in self.states.items():
            if state.containing_labels == containing_labels:
                return state.state_label
        return 'D0'

    def add_transitions(self, state: '', transition_list: [Transition]):
        self.states[state].transitions = transition_list
        for transition in transition_list:
            transition.to_state.prev.append(self)

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
        table = tabulate(data, headers=headers, tablefmt="pipe")

        with open('file.txt', 'w+') as file:
            file.write(table)
        # print(table)
        # print('\n')
