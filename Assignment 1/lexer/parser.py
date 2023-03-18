def precedence(char):
    if char in "*?+()":
        return 3
    elif char in ".":
        return 2
    elif char in "|":
        return 1
    elif char in "1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM":
        return 0


def infix_to_postfix(expression):
    expression = expression
    output = ""
    stack = []
    for curr_char in expression:
        # step 1
        if precedence(curr_char) == 0:
            output += curr_char
        else:
            # step 2b
            if curr_char == '(':
                stack.append(curr_char)
                continue
            if len(stack) == 0:
                stack.append(curr_char)
                continue
            stack_top = stack.pop()
            stack.append(stack_top)
            # step 2c
            if curr_char == ')':
                stack_top = stack.pop()
                while stack_top != '(':
                    output += stack_top
                    stack_top = stack.pop()
                continue
                # step 2d i
            else:
                while len(stack) != 0:
                    stack_top = stack.pop()
                    stack.append(stack_top)
                    if precedence(stack_top) >= precedence(curr_char) and stack_top != "(":
                        output += stack.pop()
                    else:
                        break
                stack.append(curr_char)
    while len(stack) != 0:
        output += stack.pop()

    return output


def joining_order(postfix_expression):
    operands = []
    operators = []
    for i in postfix_expression:
        if precedence(i) == 0:
            operands.append(i)
        else:
            operators.append(i)
    print(operands, operators)


# todo convert to library
def validate_regex(expression):
    for i in expression:
        brackets = 0
        if i not in "QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcvbnm?*+|.()":
            return False
        if i == '(':
            brackets += 1
        if i == ')':
            brackets -= 1
    if brackets != 0:
        return False
    return True


def add_dot(regex):
    output = ''

    for i, char in enumerate(regex):
        if char == '(' and i != 0:
            if regex[i - 1] in "|(":
                output += "("
            else:
                output += '.('
            continue
        elif char in "*?|+":
            output += char
            continue
        elif char.isalnum() and i != 0:
            if regex[i - 1] not in "(|":
                output += '.'
        output += char
    return output


# input_table = ""
# def define_input_table(expression):
#     global input_table
#     for c in expression:
#         if c not in '?*+.|':
#             input_table += c


##############################################
# nfa indicates what nfa it is i.e. a*, a or *
# state is an int which count the number of states
_nfa_block = {"nfa": str, "type": str,
              "states": [{"state": int, "input": [chr], "next_state": [int], "accepting": bool, "starting": bool}]}
nfa_table = []


def define_symbol_nfa(symbol):
    nfa_table.append({
        "nfa": symbol,
        "type": "symbol",
    })


# all nfa generating functions return the new states and count with new states added
# combination # -1 means no transition
def define_operand_nfa(operand, count):
    state_table = [{
        "state": count,
        "input": [operand],
        "next_state": [count + 1],
        "accepting": False,
        "starting": True
    }, {
        "state": count + 1,
        "input": ["#"],
        "next_state": [-1],
        "accepting": True,
        "starting": False
    }]
    nfa_table.append({"nfa": operand, "type": "operand", "states": state_table})


def build_intro_nfa_table(expression):
    count = 1
    for c in expression:
        if c in "QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890":
            define_operand_nfa(c, count)
            count += 2
        else:
            define_symbol_nfa(c)
    return count


def remove_no_move_state(nfa_block: _nfa_block):
    for state in nfa_block['states']:
        for i in range(0, len(state['input'])):
            if state['next_state'][i] == -1 and state['input'][i] == "#" and state['accepting'] == False:
                state['next_state'].pop(i)
                state['input'].pop(i)
                break


def kleen_star(nfa_block: _nfa_block, state_count: int):
    new_starting = {"state": state_count, "input": ["#"], "next_state": [state_count + 1], "accepting": False,
                    "starting": True}
    new_finishing = {"state": state_count + 1, "input": ["#"], "next_state": [-1], "accepting": True, "starting": False}
    state_count += 2

    for state in nfa_block['states']:
        # link old finish to new finish
        if state['accepting']:
            state['input'].append("#")
            state['next_state'].append(new_finishing['state'])

            # link old finish to old start
            for start in nfa_block['states']:
                if start['starting']:
                    state['input'].append("#")
                    state['next_state'].append(start['state'])

        # link new starting
        if state['starting']:
            new_starting["input"].append("#")
            new_starting["next_state"].append(state['state'])

    for state in nfa_block['states']:
        state['accepting'] = False
        state['starting'] = False

    nfa_block['states'].append(new_starting)
    nfa_block['states'].append(new_finishing)
    nfa_block['nfa'] = "(" + nfa_block['nfa'] + "*)"
    nfa_block['type'] = "expression"
    return nfa_block, state_count


def concatenate(nfa_block_a: _nfa_block, nfa_block_b: _nfa_block):
    # connect all accepting states of a to starting states of b
    for state_a in nfa_block_a['states']:
        if state_a["accepting"]:
            for state_b in nfa_block_b['states']:
                if state_b["starting"]:
                    state_a['input'].append("#")
                    state_a['next_state'].append(state_b['state'])

    # remove finishing states of A
    for state_a in nfa_block_a['states']:
        if state_a["accepting"]:
            state_a["accepting"] = False

    # remove starting states of B
    for state_b in nfa_block_b['states']:
        if state_b["starting"]:
            state_b["starting"] = False

    # generate new state block and return it
    states = nfa_block_a['states']
    for state in nfa_block_b['states']:
        states.append(state)

    return {
        "nfa": "(" + nfa_block_a["nfa"] + "." + nfa_block_b["nfa"] + ")",
        "type": "expression",
        "states": states
    }


def question_mark(nfa_block: _nfa_block):
    for start_state in nfa_block['states']:
        if start_state['starting']:
            for fin_state in nfa_block['states']:
                if fin_state['accepting']:
                    start_state['input'].append('#')
                    start_state['next_state'].append(fin_state['state'])
    nfa_block['type'] = 'expression'
    nfa_block['nfa'] = "(" + nfa_block['nfa'] + '?)'
    return nfa_block


def plus(nfa_block: _nfa_block, state_count: int):
    new_starting = {"state": state_count, "input": [], "next_state": [], "accepting": False, "starting": True}
    state_count += 1

    for start_state in nfa_block['states']:
        if start_state['starting']:
            for fin_state in nfa_block['states']:
                # link finish state to old initial
                if fin_state['accepting']:
                    fin_state['input'].append("#")
                    fin_state['next_state'].append(start_state['state'])
            # link new start state to old starting
            new_starting['input'].append("#")
            new_starting['next_state'].append(start_state['state'])

            # remove old starting states
            start_state['starting'] = False

    # add new state to block
    nfa_block['states'].append(new_starting)

    nfa_block['nfa'] = "(" + nfa_block['nfa'] + "+)"
    nfa_block['type'] = "expression"
    return nfa_block, state_count


def orr(nfa_block_a: _nfa_block, nfa_block_b: _nfa_block, state_count: int):
    # create new starting and end state
    new_start_state = {"state": state_count, "input": [], "next_state": [], "accepting": False, "starting": True}
    end_state = {"state": state_count + 1, "input": ["#"], "next_state": [-1], "accepting": True, "starting": False}
    state_count += 2

    # link initial states to new start state
    for start_state in nfa_block_a['states']:
        if start_state['starting']:
            new_start_state['input'].append("#")
            new_start_state['next_state'].append(start_state["state"])
            start_state['starting'] = False

    for start_state in nfa_block_b['states']:
        if start_state['starting']:
            new_start_state['input'].append("#")
            new_start_state['next_state'].append(start_state["state"])
            start_state['starting'] = False

    # link finishing states to new finishing state
    for fin_state in nfa_block_a['states']:
        if fin_state['accepting']:
            fin_state['input'].append("#")
            fin_state['next_state'].append(end_state['state'])
            fin_state['accepting'] = False

    for fin_state in nfa_block_b['states']:
        if fin_state['accepting']:
            fin_state['input'].append("#")
            fin_state['next_state'].append(end_state['state'])
            fin_state['accepting'] = False

    # generate new state block and return it
    states = nfa_block_a['states']
    for state in nfa_block_b['states']:
        states.append(state)
    states.append(new_start_state)
    states.append(end_state)

    return {
        "nfa": "(" + nfa_block_a["nfa"] + "|" + nfa_block_b["nfa"] + ")",
        "type": "expression",
        "states": states
    }, state_count


def print_state_table(nfa):
    count = 0
    for nfa_block_internal in nfa:
        if nfa_block_internal['type'] == 'symbol':
            continue
        count += 1
        print("\n\nblock:\t" + str(count))
        print("nfa\t\t\t\tstate\tinput\tnext_state\t\tstarting_state\t\taccepting_state")
        for states in nfa_block_internal['states']:
            for i in range(0, len(states['next_state'])):
                print(nfa_block_internal['nfa'] + "\t\t\t\t" + str(states['state']) + "\t\t" + str(
                    states['input'][i]) + "\t\t" + str(states['next_state'][i]) + "\t\t\t\t" + str(
                    states['starting']) + '\t\t\t\t' + str(states['accepting']))
    print("\n\n\n")


def parser(expression="00(01|10)*11*", validator="0.0.(0.1|1.0)*.1.1*", debug=True):
    # add dots for concatenation
    expression = add_dot(expression)
    if expression != validator and debug:
        print("ERROR################################")
        return 0

    # convert to postfix
    print("Convert from Infix to Postfix:")
    print("expression\t" + expression)
    postfix = infix_to_postfix(expression)
    print("postfix\t" + postfix)

    # generate base nfa blocks to combine
    count = build_intro_nfa_table(postfix)

    # initial nfa blocks
    print_state_table(nfa_table)

    stack = []
    for nfa_block in nfa_table:
        if nfa_block['type'] == 'symbol':
            stack.append(nfa_block)
        else:
            stack.append(nfa_block)

    i = -1
    while len(stack) != 1:
        i += 1
        symbol = stack[i]
        if symbol['nfa'] == "*":
            # print("star")
            new_block, count = kleen_star(stack[i - 1], count)
            stack.pop(i - 1)
            stack[i - 1] = new_block
            i = 0
        elif symbol['nfa'] == "?":
            # print("question_mark")
            new_block = question_mark(stack[i - 1])
            stack.pop(i - 1)
            stack[i - 1] = new_block
            i = 0
        elif symbol['nfa'] == "+":
            # print("plus")
            new_block, count = plus(stack[i - 1], count)
            stack.pop(i - 1)
            stack[i - 1] = new_block
            i = 0
        elif symbol['nfa'] == ".":
            # print("concat")
            new_block = concatenate(stack[i - 2], stack[i - 1])
            stack.pop(i - 1)
            stack.pop(i - 1)
            stack[i - 2] = new_block
            i = 0
        elif symbol['nfa'] == "|":
            # print("or")
            new_block, count = orr(stack[i - 2], stack[i - 1], count)
            stack.pop(i - 1)
            stack.pop(i - 1)
            stack[i - 2] = new_block
            i = 0

    # remove old no move states
    remove_no_move_state(stack[0])

    # print final NFA
    print("NFA:")
    print_state_table(stack)

    return stack[0]

# parser("a+|b*", "a+|b*")