from Scopes.build_scope_table import runner as build_scope
import reparse_xml as parser
from Scopes.definitions import non_terminals
from Scopes.classes import VariableTable
import copy
import array

ast_tree: dict | None
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
                if not (sub_contents[0] == 'SEQ' and sub_contents[1]['id'] in skip_list):
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


def parse_vars(tree: dict, current_node: str, var_table: VariableTable, allow_procs=False):
    if current_node == 'ALGO':
        if 'SEQ' in tree and 'SEQ' in tree['SEQ'] and has_if(tree['SEQ']['ALGO']):
            if validate_boolexpr(tree['SEQ']['ALGO']['INSTR']['BRANCH']['BOOLEXPR'], var_table):
                raise Exception('Invalid Bool Expr')

            if not has_if_else(tree['SEQ']['ALGO']):
                # Rule 28 - only then
                table_1 = copy.copy(var_table)
                # parse if
                parse_vars(tree['SEQ']['ALGO']['INSTR'], 'INSTR', table_1)
                # parse below if
                parse_vars(tree['SEQ']['SEQ'], 'SEQ', var_table)
                var_table.merge_tables(table_1.get_vars())
            else:
                # Rule 29 - then / else -- get matching vars and then split and parse
                table_1 = copy.copy(var_table)
                table_2 = copy.copy(var_table)

                # parse then
                parse_vars(tree['SEQ']['ALGO']['INSTR']['BRANCH']['ALGO'], 'ALGO', table_1)
                # parse else
                parse_vars(tree['SEQ']['ALGO']['INSTR']['BRANCH']['ELSE']['ALGO'], 'ALGO', table_2)

                # match diff
                new_table = var_table.merge_diff(table_1.get_vars(), table_2.get_vars())

                # parse below if
                parse_vars(tree['SEQ']['SEQ'], 'SEQ', var_table.set_table(new_table))

                var_table.merge_tables(table_1)
                var_table.merge_tables(table_2)
            return

        if 'SEQ' in tree and 'SEQ' in tree['SEQ'] and has_while(tree['SEQ']['ALGO']):
            if validate_boolexpr(tree['SEQ']['ALGO']['INSTR']['LOOP']['BOOLEXPR'], var_table):
                raise Exception('Invalid Bool Expr')
            # Rule 27 - while split and rebuild table
            table_1 = copy.copy(var_table)
            # parse while
            parse_vars(tree['SEQ']['ALGO']['INSTR']['LOOP']['ALGO'], 'ALGO', table_1)
            # parse after
            parse_vars(tree['SEQ']['SEQ'], 'SEQ', var_table)
            var_table.merge_tables(table_1)
            return

        if 'CALL' in tree['INSTR']:
            # TODO later due to complexity
            # name = f"p{build_call_name(tree['INSTR']['CALL']['DIGITS'])}"
            # parse_call(name, var_table)
            return

    ##########################################################################
    # Rules 22,23
    if current_node == 'LOOP':
        validate_boolexpr(tree['BOOLEXPR'], var_table)
        parse_vars(tree['ALGO'], 'ALGO', var_table)
        return

    if current_node == 'BRANCH':
        validate_boolexpr(tree['BOOLEXPR'], var_table)
        parse_vars(tree['ALGO'], 'ALGO', var_table)
        if 'ELSE' in tree:
            parse_vars(tree['ELSE'], 'ELSE', var_table)
        return

    ##########################################################################
    # Rule 21 -- Give value
    if current_node == 'INPUT':
        name = build_call_name(tree['NUMVAR']['DIGITS'])
        var_table.init_var(name, tree['NUMVAR']['id'])
        return

    ##########################################################################
    # Rule 20 -- check has values
    if current_node == 'OUTPUT':
        if 'VALUE' in tree:
            name = f"n{build_call_name(tree['NUMVAR']['DIGITS'])}"
            if not var_table.is_defined(f'n{name}', tree['NUMVAR']['id']):
                raise Exception(f'{name} undefined')
        elif 'TEXT' in tree:
            name = f"s{build_call_name(tree['STRINGV']['DIGITS'])}"
            if not var_table.is_defined(f's{name}', tree['STRINGV']['id']):
                raise Exception(f'{name} undefined')
        return

    ##########################################################################
    # Rule 2
    if current_node == 'ASSIGN':
        if 'NUMVAR' in tree:
            name = f"n{build_call_name(tree['NUMVAR']['DIGITS'])}"
            if validate_numexpr(tree['NUMEXPR'], var_table):
                var_table.init_var(name, tree['NUMVAR']['id'])
                return
            else:
                raise Exception(f'invalid expression n{name}')
        elif 'BOOLVAR' in tree:
            name = f"b{build_call_name(tree['BOOLVAR']['DIGITS'])}"
            if validate_boolexpr(tree['BOOLEXPR'], var_table):
                var_table.init_var(name, tree['BOOLVAR']['id'])
                return
            else:
                raise Exception(f'invalid expression n{name}')
        elif 'STRINGV' in tree:
            name = f"s{build_call_name(tree['STRINGV']['DIGITS'])}"
            if validate_stri(tree['STRI'], var_table):
                var_table.init_var(name, tree['STRINGV']['id'])
                return
            else:
                raise Exception(f'invalid expression n{name}')

    ##########################################################################
    # Procs are processed with calls only
    if current_node == 'PROC' and allow_procs:
        return

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


# expects numexpr
def validate_numexpr(tree: dict, var_table: VariableTable):
    if 'DECNUM' in tree:
        return True
    if 'NUMVAR' in tree:
        name = f"n{build_call_name(tree['NUMVAR']['DIGITS'])}"
        return var_table.is_defined(name, tree['NUMVAR']['id'])
    if 'NUMEXPR' in tree and tree['NUMEXPR'] is array:
        return validate_numexpr(tree['NUMEXPR'][0], var_table) and validate_numexpr(tree['NUMEXPR'][1], var_table)
    raise False


# expects boolexpr
def validate_boolexpr(tree: dict, var_table: VariableTable):
    if 'LOGIC' in tree:
        if 'BOOLVAR' in tree['LOGIC']:
            name = f"n{build_call_name(tree['LOGIC']['BOOLVAR']['DIGITS'])}"
            return var_table.is_defined(name, tree['LOGIC']['BOOLVAR']['id'])
        elif 'terminal' in tree['LOGIC']:
            if 'T' == tree['LOGIC']['terminal']['value'] or 'F' == tree['LOGIC']['terminal']['value']:
                return True
        if 'BOOLEXPR' in tree:
            if tree['BOOLEXPR'] is array:
                return validate_boolexpr(tree['BOOLEXPR'][0], var_table) and validate_boolexpr(tree['BOOLEXPR'][1],
                                                                                               var_table)
            else:
                return validate_boolexpr(tree['BOOLEXPR'], var_table)
    elif 'CMPR' in tree:
        if 'NUMEXPR' in tree['CMPR']:
            return validate_numexpr(tree['CMPR']['NUMEXPR'][0], var_table) and validate_numexpr(
                tree['CMPR']['NUMEXPR'][1], var_table)
    return False


def validate_stri(tree: dict, var_table: VariableTable):
    return True


# expects digits
def build_call_name(tree: dict):
    name = tree['D']['terminal']['value']
    name_iter = tree.copy()
    while 'MORE' in iter:
        name_iter = name_iter['MORE']['DIGITS']
        name += name_iter['D']['terminal']['value']
    return name


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
