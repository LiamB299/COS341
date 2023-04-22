import tabulate


class Variable:
    def __init__(self, label, id, expression, scope, defined):
        self.label = label
        self.id = id
        self.expression = expression
        self.scope = scope
        self.defined = defined

    def print(self):
        return [
            self.label,
            self.id,
            self.scope,
            self.defined
        ]


class VariableTable:

    def __init__(self):
        self.variables = []

    def add_var(self, var: Variable):
        comp_var: Variable
        for comp_var in self.variables:
            if comp_var.label == var.label:
                if var.defined:
                    comp_var.expression = var.expression
                return
        self.variables.append(var)

    def print(self):
        data = []
        for var in self.variables:
            data.append(var.print())

        headings = ['Label', 'ID', 'Scope', 'Is defined']

        print(tabulate.tabulate(data, headings))
        print()


class Procedure:

    def __init__(self, label, id, parent_scope):
        self.label = label
        self.id: int
        self.id = id
        self.parent_scope: int
        self.parent_scope = parent_scope
        self.called = False

    def print(self):
        return [
            self.label,
            self.id,
            self.parent_scope,
            self.called
        ]


class ProcedureTable:

    def __init__(self):
        self.procs = []

    def add_proc(self, proc: Procedure):
        comp_proc: Procedure
        for comp_proc in self.procs:
            if comp_proc.label == proc.label and comp_proc.parent_scope == proc.parent_scope:
                raise Exception(f"{comp_proc.id} naming conflict with {proc.id}")
            if self.find_parent_scope(proc.parent_scope, proc.label) >= 0:
                raise Exception(f"{comp_proc.id} naming conflict with {proc.id}")

        self.procs.append(proc)

    def set_called(self, id: int):
        for proc in self.procs:
            if proc.id == id:
                proc.called = True

    def find_parent_scope(self, parent_scope: int, label):
        for proc in self.procs:
            if proc.id == parent_scope:
                for outer_proc in self.procs:
                    if outer_proc.parent_scope == proc.parent_scope and outer_proc.label == label:
                        return outer_proc.id
        return -1

    def is_parent_scope(self, scope: int, label):
        for proc in self.procs:
            if proc.id == int(scope) and proc.label == label:
                raise Exception('Calling Parent Procedure')

    def find_proc(self, scope: int, label):
        # check current scope
        for proc in self.procs:
            if proc.parent_scope == scope and proc.label == label:
                return proc.id

        # get parent and check procs in their scope for siblings call
        return self.find_parent_scope(scope, label)

    def add_error(self, scope: int, label, message):
        for proc in self.procs:
            if proc.parent_scope == scope and proc.label == label:
                proc.error_infos.append(message)

    def print(self):
        data = []
        for proc in self.procs:
            data.append(proc.print())

        headings = ['Label', 'ID', 'Scope ID', 'Is Called']

        table = tabulate.tabulate(data, headings)
        print(table)
        print('\n')
