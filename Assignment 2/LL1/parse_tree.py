class T_node:

    is_terminal = True
    def __init__(self, label):
        self.label = label
        self.matched = False

    def match(self, symbol):
        if symbol == self.label:
            self.matched = True
        return self.matched


class NT_node:
    is_terminal = False
    def __init__(self, label):
        self.label = label
        self.children : NT_node | T_node = []

    def add_children(self, children):
        self.children = children
