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
        self.id = id
        self.parent_scope = parent_scope
        self.error_infos = []
        self.called = False

    def print(self):
        return [
            self.label,
            self.id,
            self.parent_scope,
            '',
            self.called
        ]


class ProcedureTable:

    def __init__(self):
        self.procs = []

    def add_proc(self, proc: Procedure):
        comp_proc: Procedure
        for comp_proc in self.procs:
            if comp_proc.label == proc.label:
                if comp_proc.parent_scope == proc.parent_scope:
                    comp_proc.error_infos.append(f"{comp_proc.id} naming conflict with {proc.id}")
                    proc.error_infos.append(f"{proc.id} naming conflict with {comp_proc.id}")
        self.procs.append(proc)

    def find_proc(self, scope, id):
        for proc in self.procs:
            if proc.parent_scope == scope and proc.id == id:
                return True
        return False

    def print(self):
        data = []
        for proc in self.procs:
            data.append(proc.print())

        headings = ['Label', 'ID', 'Scope ID', 'Errors', 'Is Called']

        table = tabulate.tabulate(data, headings)
        print(table)
        print('\n')
