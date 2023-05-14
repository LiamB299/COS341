from Scopes.parse_xml import read_tree
from Scopes.classes import *
from Scopes.definitions import non_terminals
from LL1.LL1_parse import runner as parser
from Scopes.html_writer import HtmlWriter


def build_assigned_var(sub_tree: {}, var_table: VariableTable):
    var = ''
    expression: {}
    var_id = -1
    if 'BOOLVAR' in sub_tree:
        var += sub_tree['BOOLVAR']['terminal']['#text']
        variable = sub_tree['BOOLVAR']['DIGITS']
        expression = sub_tree['BOOLEXPR']
        var_id = sub_tree['BOOLVAR']['@id']
    elif 'STRINGV' in sub_tree:
        var += sub_tree['STRINGV']['terminal']['#text']
        variable = sub_tree['STRINGV']['DIGITS']
        expression = sub_tree['STRI']
        var_id = sub_tree['STRINGV']['@id']
    else:
        var += sub_tree['NUMVAR']['terminal']['#text']
        variable = sub_tree['NUMVAR']['DIGITS']
        expression = sub_tree['NUMEXPR']
        var_id = sub_tree['NUMVAR']['@id']

    while 'MORE' in variable:
        var += variable['D']['terminal']['#text']
        variable = variable['MORE']['DIGITS']
    var += variable['D']['terminal']['#text']

    var_table.add_var(Variable(var, var_id, "", 0, False))

    return 0


def find_defined_variables(root_key: str, tree: {}, var_table: VariableTable, parent_id=0):
    if root_key in ['ASSIGN']:
        build_assigned_var(tree, var_table)
        return

    contents = tree.items()
    for sub_contents in list(contents):
        if not sub_contents[0] in non_terminals:
            continue
        else:
            if isinstance(sub_contents[1], dict):
                find_defined_variables(sub_contents[0], sub_contents[1], var_table, parent_id)
            else:
                for item in sub_contents[1]:
                    find_defined_variables(sub_contents[0], item, var_table, parent_id)


def build_referenced_var(sub_tree: {}, var_table: VariableTable):
    var = ''
    var_id = -1
    if 'BOOLVAR' in sub_tree:
        var += sub_tree['BOOLVAR']['terminal']['#text']
        variable = sub_tree['BOOLVAR']['DIGITS']
        var_id = sub_tree['BOOLVAR']['@id']
    elif 'STRINGV' in sub_tree:
        var += sub_tree['STRINGV']['terminal']['#text']
        variable = sub_tree['STRINGV']['DIGITS']
        var_id = sub_tree['STRINGV']['@id']
    else:
        var += sub_tree['NUMVAR']['terminal']['#text']
        variable = sub_tree['NUMVAR']['DIGITS']
        var_id = sub_tree['NUMVAR']['@id']

    while 'MORE' in variable:
        var += variable['D']['terminal']['#text']
        variable = variable['MORE']['DIGITS']
    var += variable['D']['terminal']['#text']

    var_table.add_var(Variable(var, var_id, "", 0, False))

    return 0


def find_referenced_variables(root_key: str, tree: {}, var_table: VariableTable, parent_id=0):
    if root_key in ['ASSIGN']:
        if 'BOOLVAR' in tree:
            find_referenced_variables('BOOLEXPR', tree['BOOLEXPR'], var_table, parent_id)
        elif 'STRINGV' in tree:
            find_referenced_variables('STRI', tree['STRI'], var_table, parent_id)
        else:
            find_referenced_variables('NUMEXPR', tree['NUMEXPR'], var_table, parent_id)
        return

    if root_key in ['LOGIC']:
        a = 1

    if root_key in ['NUMVAR', 'BOOLVAR', 'STRINGV']:
        build_referenced_var({root_key: tree}, var_table)
        return

    contents = tree.items()
    for sub_contents in list(contents):
        if not sub_contents[0] in non_terminals:
            continue
        else:
            if isinstance(sub_contents[1], dict):
                find_referenced_variables(sub_contents[0], sub_contents[1], var_table, parent_id)
            else:
                for item in sub_contents[1]:
                    find_referenced_variables(sub_contents[0], item, var_table, parent_id)


def build_defined_proc(sub_tree: {}, proc_table: ProcedureTable, parent_id):
    var = sub_tree['terminal'][0]['#text']
    var_id = int(sub_tree['@id'])
    variable = sub_tree['DIGITS']

    while 'MORE' in variable:
        var += variable['D']['terminal']['#text']
        variable = variable['MORE']['DIGITS']
    var += variable['D']['terminal']['#text']

    proc_table.add_proc(Procedure(var, var_id, parent_id))

    return 0


def find_procs(root_key: str, tree: {}, proc_table: ProcedureTable, parent_id=0):
    if root_key in ['PROC']:
        build_defined_proc(tree, proc_table, parent_id)
        parent_id = tree['@id']
        find_procs('PROGR', tree['PROGR'], proc_table, parent_id)
        return

    contents = tree.items()
    for sub_contents in list(contents):
        if not sub_contents[0] in non_terminals:
            continue
        else:
            if isinstance(sub_contents[1], dict):
                find_procs(sub_contents[0], sub_contents[1], proc_table, parent_id)
            else:
                for item in sub_contents[1]:
                    find_procs(sub_contents[0], item, proc_table, parent_id)


def validate_proc_call(sub_tree: {}, proc_table: ProcedureTable, parent_id=0):
    var = 'p'
    variable = sub_tree['DIGITS']

    while 'MORE' in variable:
        var += variable['D']['terminal']['#text']
        variable = variable['MORE']['DIGITS']
    var += variable['D']['terminal']['#text']

    # siblings calling each other
    # parent calling children
    proc_id = proc_table.find_proc(int(parent_id), var)
    # proc_table.is_parent_scope(int(parent_id), var)
    if proc_id < 0:
        raise Exception(int(parent_id), var, f'The procedure {var} has no corresponding declaration in this scope: {int(parent_id)}')
    else:
        proc_table.set_called(proc_id)

    return 0


def find_calls(root_key: str, tree: {}, proc_table: ProcedureTable, parent_id=0):
    if root_key in ['PROC']:
        parent_id = tree['@id']

    if root_key in ['CALL']:
        validate_proc_call(tree, proc_table, parent_id)
        return

    contents = tree.items()
    for sub_contents in list(contents):
        if not sub_contents[0] in non_terminals:
            continue
        else:
            if isinstance(sub_contents[1], dict):
                find_calls(sub_contents[0], sub_contents[1], proc_table, parent_id)
            else:
                for item in sub_contents[1]:
                    find_calls(sub_contents[0], item, proc_table, parent_id)


def runner(filename: str):
    try:
        parser(file=filename)

        ast_tree = read_tree()
        var_table = VariableTable()

        #print('Find Vars...')
        # pass 1: define vars
        find_defined_variables(list(ast_tree.keys())[0], ast_tree.copy(), var_table, 0)

        # pass 2: check vars in expressions, call logic error if not defined
        find_referenced_variables(list(ast_tree.keys())[0], ast_tree, var_table, 0)
        # var_table.print()

        print('Find Procs')
        # pass 3: build procs and scopes
        proc_table = ProcedureTable()
        find_procs(list(ast_tree.keys())[0], ast_tree, proc_table, 0)

        # pass 4: check calls are valid
        find_calls(list(ast_tree.keys())[0], ast_tree, proc_table, 0)

        # proc_table.print()

        # writer = HtmlWriter()
        # writer.write_vars(var_table)
        # writer.write_procs(proc_table)
        # print('Tables written to output.html...')
        # input()

        return var_table, proc_table
    except Exception as e:
        print('ERROR:\n')
        raise e

