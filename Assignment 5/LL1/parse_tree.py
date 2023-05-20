class node:
    count = 0

    def __init__(self):
        self.id = node.count
        node.count += 1


class T_node(node):
    is_terminal = True

    def __init__(self, label):
        super().__init__()
        self.label = label


class NT_node(node):
    is_terminal = False

    def __init__(self, label):
        super().__init__()
        self.label = label
        self.children: NT_node | T_node = []

    def add_children(self, children):
        self.children = children
