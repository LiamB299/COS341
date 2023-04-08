from tabulate import tabulate


class NfaState:
    symbol_transition = ""
    state_label = ""
    terminal_transition = False
    finishing = False
    start = False
    finishing_number = -1
    next = 0
    prev = 0
    epsilon_transitions = []

    def __init__(self, symbol, label, terminal):
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
    start_symbol: NfaState = 0
    count = 0

    def append_symbol(self, symbol: NfaState):
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