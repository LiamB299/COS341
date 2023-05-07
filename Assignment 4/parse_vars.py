from Scopes.build_scope_table import runner as build_scope
import reparse_xml as parser
from Scopes.definitions import non_terminals
from Scopes.classes import VariableTable
import copy


ast_tree = None


def prune_tree(tree: dict, key: str, skip_list):
    if key == 'ALGO':
        # base halt case
        if 'terminal' in tree['INSTR'] and tree['INSTR']['terminal']['value'] == 'h':
            if 'SEQ' in tree:
                skip_list.append(tree['SEQ']['id'])
                del tree['SEQ']
                return

        if 'BRANCH' in tree['INSTR']:
            if 'ELSE' not in tree['INSTR']['BRANCH']:
                if find_halt(tree['INSTR']['BRANCH']['ALGO']):
                    if 'SEQ' in tree:
                        skip_list.append(tree['SEQ']['id'])
                        del tree['SEQ']
                        return

            if find_halt(tree['INSTR']['BRANCH']['ALGO']):
                if find_halt(tree['INSTR']['BRANCH']['ELSE']['ALGO']):
                    if 'SEQ' in tree:
                        skip_list.append(tree['SEQ']['id'])
                        del tree['SEQ']
                        return

    contents = tree.copy().items()
    for sub_contents in list(contents):
        if not sub_contents[0] in non_terminals:
            continue
        else:
            if isinstance(sub_contents[1], dict):
                if not(sub_contents[0] == 'SEQ' and sub_contents[1]['id'] in skip_list):
                    prune_tree(sub_contents[1], sub_contents[0], skip_list)
            else:
                for item in sub_contents[1]:
                    if not (sub_contents[0] == 'SEQ' and sub_contents[1]['id'] in skip_list):
                        prune_tree(item, sub_contents[0], skip_list)

    return tree


# expects algo statements
def find_halt(tree: dict):
    if 'terminal' in tree['INSTR'] and tree['INSTR']['terminal']['value'] == 'h':
        return True

    if 'SEQ' in tree:
        return find_halt(tree['SEQ']['ALGO'])

    return False

############################################################################


def parse_vars(tree: dict, current_node: str, var_table: VariableTable):
    if current_node == 'ALGO':
        if 'SEQ' in tree and 'SEQ' in tree['SEQ'] and has_if(tree['SEQ']['ALGO']):
            if not has_if_else(tree['SEQ']['ALGO']):
                # Rule 28 - only then
                table_1 = copy.copy(var_table)
                # parse if
                parse_vars(tree['SEQ']['ALGO']['INSTR'], 'INSTR', table_1)
                # parse below if
                parse_vars(tree['SEQ']['SEQ'], 'SEQ', var_table)
                # TODO merge tables
            else:
                # Rule 29 - then / else -- get matching vars and then split and parse
                # TODO match vars in then / else
                to_pass_vars = var_then_else(tree['SEQ']['ALGO'])
                table_1 = copy.copy(var_table)
                # parse if
                parse_vars(tree['SEQ']['ALGO']['INSTR'], 'INSTR', table_1)
                # parse below if
                parse_vars(tree['SEQ']['SEQ'], 'SEQ', var_table)
                # TODO merge tables
            return

        if 'SEQ' in tree and 'SEQ' in tree['SEQ'] and has_while(tree['SEQ']['ALGO']):
            # Rule 27 - while split and rebuild table
            table_1 = copy.copy(var_table)
            # parse while
            parse_vars(tree['SEQ']['ALGO']['INSTR'], 'INSTR', table_1)
            # parse while
            parse_vars(tree['SEQ']['SEQ'], 'SEQ', var_table)
            # TODO merge tables
            return

        if current_node == 'CALL':
            parse_call()

    contents = tree.copy().items()
    for sub_contents in list(contents):
        if not sub_contents[0] in non_terminals:
            continue
        else:
            if isinstance(sub_contents[1], dict):
                parse_vars(sub_contents[1], sub_contents[0], var_table)
            else:
                for item in sub_contents[1]:
                    parse_vars(item, sub_contents[0], var_table)


def has_if(tree: dict):
    if 'BRANCH' in tree['INSTR']:
        return True
    return False


def has_while(tree: dict):
    if 'LOOP' in tree['INSTR']:
        return True
    return False


def has_if_else(tree: dict):
    if 'BRANCH' in tree['INSTR']:
        if 'ELSE' in tree['INSTR']['BRANCH']:
            return True
    return False


def var_then_else(tree: dict):

    return False


# calls should have been validated in the last prac
def parse_call(var_table: VariableTable):



def runner():
    global ast_tree

    var_table, proc_table = build_scope(filename='test_cases/t1')
    ast_tree = parser.read_tree('output.xml')

    # Rule 24 - prune tree for halts
    skip_list = []
    ast_tree = prune_tree(ast_tree, 'PROGR', skip_list)

    # Parse for vars



    return print(proc_table)


if __name__ == '__main__':
    runner()
