from Scopes.build_scope_table import runner as build_scope
from Scopes.html_writer import HtmlWriter
import reparse_xml as parser
from Scopes.definitions import non_terminals
from Scopes.classes import VariableTable, ProcedureTable

ast_tree: dict | None
ast_tree = None
proc_table = ProcedureTable | None
proc_list = []


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

    duplicate = tree.copy()
    contents = duplicate.items()
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


def build_proc_list(tree: dict, current_node: str):
    if current_node == 'PROC':
        proc_list.append(tree)
    else:
        contents = tree.copy().items()
        for sub_contents in list(contents):
            if not sub_contents[0] in non_terminals:
                continue
            else:
                if isinstance(sub_contents[1], dict):
                    build_proc_list(sub_contents[1], sub_contents[0])
                else:
                    for item in sub_contents[1]:
                        build_proc_list(item, sub_contents[0])


# expects algo statements
def find_halt(tree: dict):
    if 'terminal' in tree['INSTR'] and tree['INSTR']['terminal']['value'] == 'h':
        return True

    if 'SEQ' in tree:
        return find_halt(tree['SEQ']['ALGO'])

    return False


############################################################################
def parse_vars(tree: dict, current_node: str, var_table: VariableTable, allow_procs=False, scope=0):
    if current_node == 'PROC':
        scope = tree['id']
    if current_node == 'ALGO':
        if 'SEQ' in tree and has_if(tree):
            if not validate_boolexpr(tree['INSTR']['BRANCH']['BOOLEXPR'], var_table):
                raise Exception('Invalid Bool Expr')

            if not has_if_else(tree):
                # Rule 28 - only then
                table_1 = VariableTable()
                table_1.set_table(var_table.get_vars().copy())
                # parse if
                parse_vars(tree['INSTR']['BRANCH']['ALGO'], 'ALGO', table_1, scope=scope)
                # parse below if
                parse_vars(tree['SEQ'], 'SEQ', var_table, scope=scope)
                var_table.merge_tables(table_1.get_vars())
            else:
                # Rule 29 - then / else -- get matching vars and then split and parse
                table_1 = VariableTable()
                table_1.set_table(var_table.get_vars().copy())
                table_2 = VariableTable()
                table_2.set_table(var_table.get_vars().copy())

                # parse then
                parse_vars(tree['INSTR']['BRANCH']['ALGO'], 'ALGO', table_1, scope=scope)
                # parse else
                parse_vars(tree['INSTR']['BRANCH']['ELSE']['ALGO'], 'ALGO', table_2, scope=scope)

                # match diff
                new_table = var_table.merge_diff(table_1.get_vars(), table_2.get_vars())
                var_table.set_table(new_table)

                # parse below if
                parse_vars(tree['SEQ'], 'SEQ', var_table, scope=scope)

                var_table.merge_tables(table_1.get_vars())
                var_table.merge_tables(table_2.get_vars())
            return

        # if 'SEQ' in tree and 'SEQ' in tree['SEQ'] and has_while(tree['SEQ']['ALGO']):
        if 'SEQ' in tree and 'LOOP' in tree['INSTR']:
            if not validate_boolexpr(tree['INSTR']['LOOP']['BOOLEXPR'], var_table):
                raise Exception('Invalid Bool Expr')
            # Rule 27 - while split and rebuild table
            table_1 = VariableTable()
            table_1.set_table(var_table.get_vars().copy())
            # parse while
            parse_vars(tree['INSTR']['LOOP']['ALGO'], 'ALGO', table_1, scope=scope)
            # parse after
            parse_vars(tree['SEQ'], 'SEQ', var_table, scope=scope)
            var_table.merge_tables(table_1.get_vars())
            return

        if 'CALL' in tree['INSTR']:
            # TODO later due to complexity
            name = f"p{build_call_name(tree['INSTR']['CALL']['DIGITS'])}"
            parse_call(name, var_table, scope)
            parse_vars(tree['SEQ'], 'SEQ', var_table, scope=scope)
            return

    ##########################################################################
    # Rules 22,23
    if current_node == 'LOOP':
        validate_boolexpr(tree['BOOLEXPR'], var_table)
        parse_vars(tree['ALGO'], 'ALGO', var_table, scope=scope)
        return

    if current_node == 'BRANCH':
        validate_boolexpr(tree['BOOLEXPR'], var_table)
        parse_vars(tree['ALGO'], 'ALGO', var_table, scope=scope)
        if 'ELSE' in tree:
            parse_vars(tree['ELSE'], 'ELSE', var_table, scope=scope)
        return

    ##########################################################################
    # Rule 21 -- Give value
    if current_node == 'INPUT':
        name = f"n{build_call_name(tree['NUMVAR']['DIGITS'])}"
        var_table.init_var(name, tree['NUMVAR']['id'])
        return

    ##########################################################################
    # Rule 20 -- check has values
    if current_node == 'OUTPUT':
        if 'VALUE' in tree:
            name = f"n{build_call_name(tree['VALUE']['NUMVAR']['DIGITS'])}"
            if not var_table.is_defined(name, tree['VALUE']['NUMVAR']['id']):
                raise Exception(f'{name} undefined')
        elif 'TEXT' in tree:
            name = f"s{build_call_name(tree['TEXT']['STRINGV']['DIGITS'])}"
            if not var_table.is_defined(name, tree['TEXT']['STRINGV']['id']):
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
                raise Exception(f'invalid expression for {name}')
        elif 'BOOLVAR' in tree:
            name = f"b{build_call_name(tree['BOOLVAR']['DIGITS'])}"
            if validate_boolexpr(tree['BOOLEXPR'], var_table):
                var_table.init_var(name, tree['BOOLVAR']['id'])
                return
            else:
                raise Exception(f'invalid expression for {name}')
        elif 'STRINGV' in tree:
            name = f"s{build_call_name(tree['STRINGV']['DIGITS'])}"
            if validate_stri(tree['STRI'], var_table):
                var_table.init_var(name, tree['STRINGV']['id'])
                return
            else:
                raise Exception(f'invalid expression for {name}')

    ##########################################################################
    # Procs are processed with calls only
    if current_node == 'PROC' and not allow_procs:
        return

    contents = tree.copy().items()
    for sub_contents in list(contents):
        if not sub_contents[0] in non_terminals:
            continue
        else:
            if isinstance(sub_contents[1], dict):
                parse_vars(sub_contents[1], sub_contents[0], var_table, scope=scope)
            else:
                for item in sub_contents[1]:
                    parse_vars(item, sub_contents[0], var_table, scope=scope)


def parse_call(name: str, var_table: VariableTable, scope: int):
    global proc_table
    global proc_list
    # find proc
    id, proc_scope = proc_table.find_call_proc(name, scope)
    for proc in proc_list:
        if int(proc['id']) == id:
            parse_vars(proc['PROGR'], 'PROGR', var_table, False, proc_scope)
            return


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
    if 'NUMEXPR' in tree and isinstance(tree['NUMEXPR'], list):
        return validate_numexpr(tree['NUMEXPR'][0], var_table) and validate_numexpr(tree['NUMEXPR'][1], var_table)
    raise False


# expects boolexpr
def validate_boolexpr(tree: dict, var_table: VariableTable):
    if 'LOGIC' in tree:
        if 'BOOLVAR' in tree['LOGIC']:
            name = f"b{build_call_name(tree['LOGIC']['BOOLVAR']['DIGITS'])}"
            return var_table.is_defined(name, tree['LOGIC']['BOOLVAR']['id'])
        elif 'terminal' in tree['LOGIC']:
            if isinstance(tree['LOGIC']['terminal'], dict) and ('T' == tree['LOGIC']['terminal']['value'] or 'F' == tree['LOGIC']['terminal']['value']):
                return True
        if 'BOOLEXPR' in tree['LOGIC']:
            if isinstance(tree['LOGIC']['BOOLEXPR'], list):
                check1 = validate_boolexpr(tree['LOGIC']['BOOLEXPR'][0], var_table)
                check2 = validate_boolexpr(tree['LOGIC']['BOOLEXPR'][1], var_table)
                return check1 and check2
            else:
                return validate_boolexpr(tree['LOGIC']['BOOLEXPR'], var_table)
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
    while 'MORE' in name_iter:
        name_iter = name_iter['MORE']['DIGITS']
        name += name_iter['D']['terminal']['value']
    return name


def runner():
    global ast_tree
    global proc_table

    try:
        var_table, proc_table = build_scope('')
        ast_tree = parser.read_tree('output.xml')

        # Rule 24 - prune tree for halts
        skip_list = []
        ast_tree = prune_tree(ast_tree, 'PROGR', skip_list)

        # Build Proc list
        build_proc_list(ast_tree, 'PROGR')

        var_table.clear_table()

        # Parse for vars
        print('Build Vars')
        parse_vars(ast_tree, 'PROGR', var_table, False, 0)

        # Print HTML
        writer = HtmlWriter()
        writer.write_procs(proc_table)
        writer.write_vars(var_table)
        del writer
        print('Variables processed')
        input('\nPress enter to close')

    except Exception as e:
        print('\nProcessing Error')
        # print('This probably fell through from an error above')
        print(e)
        input('\nPress enter to close')

    return 0


if __name__ == '__main__':
    runner()
