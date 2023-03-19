from parser import parser, _nfa_block
from itertools import chain, combinations


def generate_powerset(nfa: _nfa_block):
    # get number of states
    n_states = len(nfa['states'])

    # normal set
    normal_set = []

    # generate set
    for i in range(1, n_states + 1):
        normal_set.append(i)

    # generate powerset
    # credit: https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    # powerset = []
    # x = len(normal_set)
    # for i in range(1 << x):
    #     powerset.append([normal_set[j] for j in range(x) if (i & (1 << j))])

    s = list(normal_set)
    items = list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))
    powerset = [list(i) for i in items if True]

    return powerset


def generate_basic_closures(nfa: _nfa_block):
    # get number of states
    n_states = len(nfa['states'])

    states_closures = []
    for i in range(1, n_states + 1):
        current_closure = []
        visit_state(nfa, i, current_closure)
        states_closures.append({'state': i, 'closure': current_closure})

    return states_closures


def visit_state(nfa: _nfa_block, current_state: int, visited: []):
    # this state is visited
    visited.append(current_state)

    # get current state
    for state in nfa['states']:
        if state['state'] == current_state:
            break

    # if state has epsilon transition go to it
    for i, input_char in enumerate(state['input']):
        if input_char == '#' and state['next_state'][i] == -1:
            continue
        if input_char == "#":
            if state['next_state'][i] not in visited:
                visit_state(nfa, state['next_state'][i], visited)


def generate_power_closures(nfa: _nfa_block):
    # generate closures
    basic_closures = generate_basic_closures(nfa)
    # print(basic_closures)

    # generate powerset
    powerset = generate_powerset(nfa)

    power_closures = []
    # count = 1
    # for set in powerset:
    #     current_closure = []
    #     for state in set:
    #         for closure in basic_closures[state - 1]['closure']:
    #             current_closure.append(closure)
    #     res = []
    #     [res.append(x) for x in current_closure if x not in res]
    #     current_closure = res
    #     current_closure.sort()
    #     power_closures.append({"set": set, "label": count, "closure": current_closure})
    #     count += 1

    # Create a dictionary mapping each state to its closures
    closure_map = {}
    for i, closure in enumerate(basic_closures):
        closure_map[i + 1] = closure['closure']

    # Iterate over the powerset and compute closures
    power_closures = []
    for i, subset in enumerate(powerset):
        current_closure = set().union(*(closure_map[state] for state in subset))
        power_closures.append({"set": subset, "label": i, "closure": sorted(current_closure)})

    return power_closures, powerset


# check if set has accepting and/or starting state
def is_accepting_starting(nfa: _nfa_block, states: []):
    starting = False
    accepting = False

    for state in nfa["states"]:
        for set_state in states:
            if state["state"] == set_state:
                if state['accepting']:
                    accepting = True
                if state['starting']:
                    starting = True
        if accepting and starting:
            break

    return accepting, starting


# reduce the power set to only important entries
def reduce_power_set(transition_table:[], power_set: []):
    reduced_set = []
    for i, set in enumerate(power_set):
        for defined_state in transition_table:
            if defined_state['state'] in set['set'] or len(set['set']) == 1:
                reduced_set.append(power_set[i])
                break
    return reduced_set


def build_dfa(nfa: _nfa_block, power_closures):
    # dfa
    _transition_table = []

    # new state count
    count = 1

    # generate base transition table
    for state in nfa['states']:
        _input = []
        next_state = []
        # iterate through states and inputs of nfa
        for i, state_input in enumerate(state['input']):
            if state_input == "#":
                continue
            else:
                # lookup closure for state transitioned to
                find_closure = state['next_state'][i]
                for closure in power_closures:
                    # if one of single state sets and is the closure desired
                    if len(closure['set']) == 1 and closure['set'][0] == find_closure:
                        closure_set = closure['closure']
                        closure_set.sort()
                        _input.append(state_input)
                        next_state.append({"label": closure["label"], "state": closure_set})
                        break

        if len(_input) != 0:
            _transition_table.append({"state": state["state"], "input": _input, "next_state": next_state})

    # print(_transition_table)

    # power_closures = reduce_power_set(_transition_table, power_closures)

    # build new transition table
    power_transitions = []
    for closure_set in power_closures:
        bigger_trans_set_input = []
        bigger_trans_set_next_state = []
        for new_trans_state in _transition_table:
            if new_trans_state['state'] in closure_set['set']:
                for i, _input in enumerate(new_trans_state["input"]):
                    ####################################
                    # if an input is defined the transition sets must be merged
                    if _input in bigger_trans_set_input:
                        index = bigger_trans_set_input.index(_input)
                        prev_to_add = bigger_trans_set_next_state[index]['state']
                        to_merge = new_trans_state['next_state'][i]['state']
                        merged = prev_to_add + to_merge
                        merged = list(dict.fromkeys(merged))
                        merged.sort()
                        bigger_trans_set_next_state[index]['state'] = merged
                    ####################################
                    else:
                        bigger_trans_set_input.append(_input)
                        bigger_trans_set_next_state.append(
                        {"label": "", "state": new_trans_state['next_state'][i]['state']})
        power_transitions.append(
            {"state": closure_set['set'], "input": bigger_trans_set_input, "next_state": bigger_trans_set_next_state,
             "accepting": False, "starting": False})

    for old_state in nfa['states']:
        if old_state['starting']:
            for closure in power_closures:
                if len(closure['set']) == 1:
                    closure_set = closure['set'][0]
                    state_num = old_state['state']
                    if closure_set == state_num:
                        start_closure = closure['closure']
                        break

    # find starting state
    start_closure.sort()
    for state in power_transitions:
        if len(state['state']) == len(start_closure):
            found = True
            for i, item in enumerate(state['state']):
                if item != start_closure[i]:
                    found = False
                    break
            if found:
                state['starting'] = True
                break

    # define accepting states
    for old_state in nfa['states']:
        if old_state['accepting']:
            find = old_state['state']
            for state in power_transitions:
                for number in state['state']:
                    if number == find:
                        state['accepting'] = True

    # turn state array into string
    for state in power_transitions:
        state['state'] = str(state['state'])
        for next_state in state['next_state']:
            next_state['state'] = str(next_state['state'])

    # return DFA
    return {
        "dfa": "un-minimized", "states": power_transitions
    }


def reduce_dfa_states(dfa):
    # find starting state
    for starting_state in dfa['states']:
        if starting_state['starting']:
            break

    # transverse dfa
    visited = [starting_state['state']]
    for transition_states in starting_state['next_state']:
        traverse_dfa(dfa, transition_states['state'], visited)

    # remove untagged states
    print("reducing states...")
    reachable_states = []
    for old_state in dfa['states']:
        for visited_state in visited:
            if visited_state == old_state['state']:
                reachable_states.append(old_state)

    dfa['states'] = reachable_states


def traverse_dfa(dfa, current_state: str, visited: []):
    for state in visited:
        if state == current_state:
            return

    # this state is visited
    visited.append(current_state)

    # get current state
    found = False
    for state in dfa['states']:
        c_state = state['state']
        if c_state == current_state:
            found = True
            break

    if not found:
        print("ERROR++++++++++++++++++++++++++++++++++++++")
        return

    # go to next state
    for transition_states in state['next_state']:
        if transition_states['state'] not in visited:
            traverse_dfa(dfa, transition_states['state'], visited)


def relabel_dfa(dfa):
    states = dfa['states']
    old_states = []

    for i, state in enumerate(states):
        old_states.append({'new_state': str(i + 1), "old_state": state['state']})
        state['state'] = str(i + 1)

    for i, state in enumerate(states):
        for next_state in state['next_state']:
            for old_state in old_states:
                if next_state['state'] == old_state['old_state']:
                    next_state['state'] = old_state['new_state']
                    break

    return dfa


def print_dfa(dfa):
    print("DFA")
    print(dfa['dfa'])
    print("state\t\t\tinput\t\t\tnext_state\t\t\tstarting\t\t\taccepting")
    for state in dfa['states']:
        if len(state['input']) != 0:
            for i, _input in enumerate(state['input']):
                print(str(state["state"]) + "\t\t\t\t\t" + str(_input) + '\t\t\t\t\t' +
                      str(state['next_state'][i]['state']) + "\t\t\t\t\t" + str(state['starting']) + "\t\t\t\t\t" + str(
                    state['accepting']))
        else:
            if state['accepting'] or state['starting']:
                print(str(state["state"]) + "\t\t\t\t\t" + "[]" + '\t\t\t\t\t' +
                      "[]" + "\t\t\t\t\t" + str(state['starting']) + "\t\t\t\t\t" + str(
                    state['accepting']))

    print('\n\n\n')
