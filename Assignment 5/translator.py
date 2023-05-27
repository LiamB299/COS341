import basic_translator
from definitions import non_terminals
from read_xml import read_tree
from Variable_checker.parse_vars import runner as process_tree

line_number = 00
label_counter = 00


def build_var_name(tree: dict):
    varname = ''
    to_iter = tree.copy()
    while 'MORE' in to_iter:
        varname += to_iter['D']['terminal']['value']
        to_iter = to_iter['MORE']['DIGITS']
    varname += to_iter['D']['terminal']['value']

    return varname


def translate_decnum(tree: dict):
    code = ''
    if 'NEG' in tree:
        code = '-' + translate_decnum(tree['NEG'])
    elif 'POS' in tree:
        code = tree['POS']['INT']['terminal']['value']
        if 'MORE' in tree['POS']['INT']:
            code += build_var_name(tree['POS']['INT']['MORE']['DIGITS'])
        code += '.'
        code += tree['POS']['D'][0]['terminal']['value']
        code += tree['POS']['D'][1]['terminal']['value']
    else:
        code = '0.00'
    return code


# def translate_logic(tree: dict):
#     code = ''
#     if 'terminal' in tree and isinstance(tree['terminal'], dict):
#         state = tree['terminal']['value']
#         if state == 'F':
#             code = '0'
#         else:
#             code = '1'
#     elif 'BOOLVAR' in tree:
#         code = f'b{build_var_name(tree["BOOLVAR"]["DIGITS"])}'
#
#     elif isinstance(tree['BOOLEXPR'], dict):
#         # op = tree['terminal'][0]['value'][0]
#         expr_code_1 = translate_expression(tree['BOOLEXPR'][0], 'BOOLEXPR')
#         code = f'(NOT ({expr_code_1}))'
#
#     else:
#         op = tree['terminal'][0]['value'][0]
#         if op == '^':
#             op = 'AND'
#         elif op == 'v':
#             op = 'OR'
#         else:
#             raise Exception('No logic operator found')
#
#         expr_code_1 = translate_expression(tree['BOOLEXPR'][0], 'BOOLEXPR')
#         expr_code_2 = translate_expression(tree['BOOLEXPR'][1], 'BOOLEXPR')
#         code = f'({expr_code_1}) {op} ({expr_code_2})'
#     return code


def translate_cmpr(tree: dict):
    op = tree['terminal'][0]['value'][0]
    if op == 'E':
        op = '='
    elif op not in ['<', '>']:
        raise Exception('No logic operator found')

    expr_code_1 = translate_expression(tree['NUMEXPR'][0], 'NUMEXPR')
    expr_code_2 = translate_expression(tree['NUMEXPR'][1], 'NUMEXPR')
    code = f'({expr_code_1}) {op} ({expr_code_2})'

    return code


def translate_stri(tree: dict):
    stringv = ''
    for char in tree['C']:
        if 'value' in char['terminal']:
            stringv += char['terminal']['value']
        else:
            stringv += " "
    return f'{stringv}'


def translate_comment(tree: dict):
    comment = ''
    for char in tree['C']:
        if 'value' in char['terminal']:
            comment += char['terminal']['value']
        else:
            comment += " "

    code = f'REM \"{comment}\"\n'
    return code


def translate_input(tree: dict):
    numvar = build_var_name(tree['NUMVAR']['DIGITS'])
    code = f'INPUT "ENTER A NUMBER"; n{numvar}\n'
    return code


def translate_output(tree: dict):
    code = ''
    if 'TEXT' in tree:
        stringv = build_var_name(tree['TEXT']['STRINGV']['DIGITS'])
        code = f'PRINT s{stringv}$\n'
    if 'VALUE' in tree:
        numv = build_var_name(tree['VALUE']['NUMVAR']['DIGITS'])
        code = f'PRINT n{numv}\n'
    return code


def translate_assign(tree: dict):
    code = ''
    if 'NUMVAR' in tree:
        numvar = build_var_name(tree['NUMVAR']['DIGITS'])
        expr_code = translate_expression(tree['NUMEXPR'], 'NUMEXPR')
        code = f'n{numvar} = {expr_code}\n'

    elif 'BOOLVAR' in tree:
        boolvar = build_var_name(tree['BOOLVAR']['DIGITS'])
        expr_code = translate_expression(tree['BOOLEXPR'], 'BOOLEXPR', f'b{boolvar}')
        # code = f'b{boolvar} = {expr_code}\n'
        return f'{expr_code}\n'
    elif 'STRINGV' in tree:
        stringv = build_var_name(tree['STRINGV']['DIGITS'])
        expr_code = translate_expression(tree['STRI'], 'STRI')
        code = f's{stringv} = \"{expr_code}\"\n'

    return code


def translate_call(tree: dict):
    code = ''
    cp = build_var_name(tree['DIGITS'])

    code = f'GOSUB p{cp}\n'

    return code


# expect logic condition
def translate_logic_cond(tree: dict, label_t: str, label_f: str):
    global label_counter

    if 'LOGIC' not in tree and 'CMPR' in tree:
        code = f"{translate_cmpr(tree['CMPR'])}"
        boolvar = f'b696969 = {code}'
        label_counter += 2
        # return f"{boolvar}\nIF b696969=1 THEN \nGOTO {label_t} \nENDIF\nGOTO {label_f}"
        return f"{boolvar}\nIF b696969=1 THEN GOTO {label_t}\nGOTO {label_f}"
        # 'expr' types

    if 'BOOLVAR' in tree['LOGIC']:
            return f'b{build_var_name(tree["LOGIC"]["BOOLVAR"]["DIGITS"])}'

    elif 'terminal' in tree['LOGIC'] and isinstance(tree['LOGIC']['terminal'], dict):
        state = tree['LOGIC']['terminal']['value']
        if state == 'F':
            return f'GOTO {label_f}'
        else:
            return f'GOTO {label_t}'
    # not
    elif isinstance(tree['LOGIC']['BOOLEXPR'], dict):
        return translate_logic_cond(tree['LOGIC']['BOOLEXPR'], label_f, label_t)

    else:
        op = tree['LOGIC']['terminal'][0]['value'][0]
        new_label = f"condition_label_{label_counter}"
        label_counter += 1
        if op == '^':
            code1 = translate_logic_cond(tree['LOGIC']['BOOLEXPR'][0], new_label, label_f)
            code2 = translate_logic_cond(tree['LOGIC']['BOOLEXPR'][1], label_t, label_f)
            return f"{code1}\n{new_label}\n{code2}"
        elif op == 'v':
            code1 = translate_logic_cond(tree['LOGIC']['BOOLEXPR'][0], label_t, new_label)
            code2 = translate_logic_cond(tree['LOGIC']['BOOLEXPR'][1], label_t, label_f)
            return f"{code1}\n{new_label}\n{code2}"
        else:
            raise Exception('No logic operator found')


def translate_loop(tree: dict):
    global label_counter
    label_check = f'check_while_label_{label_counter}'
    label_2 = f'label_{label_counter+1}'
    label_3 = f'label_{label_counter+2}'
    label_counter += 3

    cond_code = translate_logic_cond(tree['BOOLEXPR'], label_2, label_3)
    algo_code = translator(tree['ALGO'], 'ALGO')

    # code = f'''{label_check}:\nIF {expr_code} THEN\n{algo_code}\nGOTO {label_check}\nENDIF\n'''
    code = f'''
{label_check}:
{cond_code}
{label_2}:
{algo_code}
GOTO {label_check}
{label_3}:
'''
    return code


def translate_branch(tree: dict):
    global label_counter

    label_1 = f'label_then_{label_counter}'
    label_2 = f'label_else_{label_counter+1}'
    cond_code = translate_logic_cond(tree['BOOLEXPR'], label_1, label_2)
    if cond_code.find('IF') < 0 and cond_code[0] == 'b':
        cond_code = f'IF {cond_code} = 1 THEN GOTO {label_1}'
    algo_code = translator(tree['ALGO'], 'ALGO')
    if 'ELSE' in tree:
        label_3 = f'label_after_{label_counter+2}'
        else_code = translator(tree['ELSE']['ALGO'], 'ALGO')
        label_counter += 2

        code = f'''
{cond_code}
{label_2}:
{else_code}
GOTO {label_3}
{label_1}:
{algo_code}
{label_3}:
'''
        label_counter += 3

    else:
        label_counter += 2
        code = f'''
{cond_code}
{label_1}:
{algo_code}
{label_2}:
'''


    # cond_code = translate_logic(tree['BOOLEXPR'], 'BOOLEXPR')
    # algo_code = translator(tree['ALGO'], 'ALGO')
    #
    # else_code = ''
    # if 'ELSE' in tree:
    #     else_code = translator(tree['ELSE']['ALGO'], 'ALGO')
    #
    # label_after_else = f'after_else_{label_counter}'
    # label_counter += 1

#     code = f'''IF {cond_code} THEN
# {algo_code}
# GOTO {label_after_else}
# ENDIF
# {else_code}
# {label_after_else}:\n'''

    return code


def translate_halt():
    return 'STOP\n'


# expects proc
def translate_procedure(tree: dict):
    proc_name = build_var_name(tree['DIGITS'])

    progr_code = translator(tree, 'PROGR')

    code = f'''
SUB p{proc_name}\n
{progr_code}
RETURN
END SUB\n
    '''
    return code


# instructions contain expressions
def translate_expression(tree: dict, expression_type: str, boolname= ''):
    global label_counter
    code = ''

    if expression_type == 'NUMEXPR':
        if 'DECNUM' in tree:
            code = translate_decnum(tree['DECNUM'])
        elif 'NUMVAR' in tree:
            code += 'n'
            code += build_var_name(tree['NUMVAR']['DIGITS'])
        else:
            op = tree['terminal'][0]['value'][0]
            if op == 'a':
                op = '+'
            elif op == 'm':
                op = '*'
            elif op == 'd':
                op = '/'
            else:
                raise Exception('No math operator found')

            expr1 = translate_expression(tree['NUMEXPR'][0], 'NUMEXPR')
            expr2 = translate_expression(tree['NUMEXPR'][1], 'NUMEXPR')
            code = f'({expr1}) {op} ({expr2})'

    elif expression_type == 'BOOLEXPR':
        if 'CMPR' in tree:
            code = translate_cmpr(tree['CMPR'])
        if 'LOGIC' in tree:
            if 'terminal' in tree['LOGIC'] and isinstance(tree['LOGIC']['terminal'], dict):
                state = tree['LOGIC']['terminal']['value']
                if state == 'F':
                    return f'{boolname} = 0'
                else:
                    return f'{boolname} = 1'
            elif 'BOOLVAR' in tree['LOGIC']:
                return f'{boolname} = b{build_var_name(tree["LOGIC"]["BOOLVAR"]["DIGITS"])}'
            else:
                label_1 = f"label_{label_counter}"
                label_2 = f"label_{label_counter+1}"
                cond_code = translate_logic_cond(tree, label_1, label_2)
                return f"{boolname}=0\n{cond_code}\n{label_1}\n{boolname}=1\n{label_2}:"

    elif expression_type == 'STRI':
        code = translate_stri(tree)

    return code


# algo is a statement
def translate_statement(tree: dict):
    statement_code = ''

    if 'KOMMENT' in tree:
        statement_code = translate_comment(tree['KOMMENT'])

    if 'INPUT' in tree['INSTR']:
        statement_code += translate_input(tree['INSTR']['INPUT'])
    elif 'OUTPUT' in tree['INSTR']:
        statement_code += translate_output(tree['INSTR']['OUTPUT'])
    elif 'ASSIGN' in tree['INSTR']:
        statement_code += translate_assign(tree['INSTR']['ASSIGN'])
    elif 'CALL' in tree['INSTR']:
        statement_code += translate_call(tree['INSTR']['CALL'])
    elif 'LOOP' in tree['INSTR']:
        statement_code += translate_loop(tree['INSTR']['LOOP'])
    elif 'BRANCH' in tree['INSTR']:
        statement_code += translate_branch(tree['INSTR']['BRANCH'])
    elif 'terminal' in tree['INSTR'] and isinstance(tree['INSTR']['terminal'], dict) and tree['INSTR']['terminal'][
        'value'] == 'h':
        statement_code += translate_halt()

    return statement_code


def translator(tree: dict, current_node: str):
    source_code = ''
    if current_node == 'ALGO':
        source_code += translate_statement(tree)
        if 'SEQ' in tree:
            return source_code + translator(tree['SEQ']['ALGO'], 'ALGO')
        else:
            return source_code

    if current_node == 'PROCDEFS':
        source_code += translate_procedure(tree['PROC'])
        if 'PROCDEFS' in tree:
            return source_code + translator(tree['PROCDEFS'], 'PROCDEFS')
        else:
            return source_code

    if 'PROGR' in tree:
        source_code += translator(tree['PROGR']['ALGO'], 'ALGO')

    if 'PROGR' in tree and 'PROCDEFS' in tree['PROGR']:
        source_code += 'END\n'
        source_code += translator(tree['PROGR']['PROCDEFS'], 'PROCDEFS')

    return source_code

    # contents = tree.copy().items()
    # for sub_contents in list(contents):
    #     if not sub_contents[0] in non_terminals:
    #         continue
    #     else:
    #         if isinstance(sub_contents[1], dict):
    #             source_code += translator(sub_contents[1], sub_contents[0])
    #         else:
    #             for item in sub_contents[1]:
    #                 source_code += translator(item, sub_contents[0])
    # return source_code


def runner():
    # try:
    ast_tree = process_tree('test6')

    code = translator(ast_tree, 'PROGR')
    print(code)

    b_trans = basic_translator.BasicTranslator(code)
    b_trans.printer()

        # except Exception as e:
        #     print(e)

    return 0
    # except Exception as e:
    #     print("Processing Error")
    #     print(e)
    #     input("Press Enter to close")


if __name__ == '__main__':
    runner()
