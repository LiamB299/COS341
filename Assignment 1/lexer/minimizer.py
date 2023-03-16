from lexer import print_dfa, parser, generate_power_closures, build_dfa, relabel_dfa, reduce_dfa_states


# O(n^4)
def find_duplicates(states):
    duplicates = []
    count = 0
    found_states = []
    # iterate through states
    for i, state in enumerate(states):
        # set number
        count += 1

        # if already added to duplicate set skip
        already_found = False
        for found_state in found_states:
            if state['state'] == found_state:
                already_found = True
                break

        if already_found:
            continue

        # iterate through others
        for j, other_state in enumerate(states):
            if i == j:
                continue

            # if not the same size inputs skip
            if len(state['input']) != len(other_state['input']):
                continue

            # check input is defined
            found = False
            for _input in state['input']:
                found = False
                for compare_input in other_state['input']:
                    if _input == compare_input:
                        found = True
                        break
                if not found:
                    break

            if not found:
                continue

            same = True
            # compare next state for same input
            for l, next_state in enumerate(state['next_state']):
                for m, compare_next_state in enumerate(other_state['next_state']):

                    # same input
                    if state['input'][l] == other_state['input'][m]:
                        # same state
                        if next_state['state'] != compare_next_state['state']:
                            same = False
                            break

                if not same:
                    continue

            # check duplicates
            # add duplicates to same group
            if state['state'] not in found_states and same:
                found_states.append(state['state'])
                duplicates.append({'state':state, 'group': count})

            if other_state['state'] not in found_states and same:
                found_states.append(other_state['state'])
                duplicates.append({'state': other_state, 'group': count})

    return duplicates


def minimize(dfa):
    changed = True
    states = dfa['states']

    # repeat until no changes
    while changed:
        no_duplicates_unfinishing = False
        no_duplicates_finishing = False

        # split into finishing and non-finishing
        finishing = []
        unfinishing = []

        for state in states:
            if state['accepting']:
                finishing.append(state)
            else:
                unfinishing.append(state)

        # find duplicate states in nf
        duplicates = find_duplicates(unfinishing)

        if len(duplicates) != 0:
            new_states = update_states(states, duplicates)
            update_state_list(states, new_states)

        else:
            no_duplicates_unfinishing = True

        # do same for finishing
        duplicates = find_duplicates(finishing)

        if len(duplicates) != 0:
            new_states = update_states(states, duplicates)
            update_state_list(states, new_states)

        else:
            no_duplicates_finishing = True

        changed = not ( no_duplicates_finishing and no_duplicates_unfinishing )

    return {
        "dfa": "minimized",
        "states": states
    }


def update_states(states, duplicates):
    # remove found duplicates from state list
    for i in range(len(states) - 1, -1, -1):
        for state in duplicates:
            if states[i]['state'] == state['state']['state']:
                states.pop(i)
                break

    # merge duplicates
    new_states = merge_duplicates(duplicates)
    return new_states


def merge_duplicates(duplicates):
    new_states = []
    count = 0
    for i in range(0, len(duplicates)):
        # get duplicate set
        duplicate_set = [duplicates[i]]
        old_states = [duplicates[i]['state']['state']]
        starting = duplicates[i]['state']['starting']
        for k in range(i + 1, len(duplicates)):
            if duplicates[k]['group'] == duplicate_set[0]['group']:
                duplicate_set.append(duplicates[k])
                starting = duplicates[k]['state']['starting'] or starting
                old_states.append(duplicates[k]['state']['state'])

        # merge duplicates
        if len(duplicate_set) > 1:
            new_states.append({'state': duplicates[i]['state']['state'],
                               'input': duplicate_set[0]['state']['input'],
                                'next_state': duplicate_set[0]['state']['next_state'],
                               'accepting': duplicate_set[0]['state']['accepting'],
                               'starting': starting,
                               "old_states": old_states})

        count += 1
        i = k + 1

    return new_states


def update_state_list(states, new_states):
    # update transitions
    for state in states:
        for next_state in state['next_state']:
            for new_state in new_states:
                if next_state['state'] in new_state['old_states']:
                    # update transition
                    next_state['state'] = new_state['state']

    for state in new_states:
        for next_state in state['next_state']:
            for new_state in new_states:
                if next_state['state'] in new_state['old_states']:
                    # update transition
                    next_state['state'] = new_state['state']

    for state in new_states:
        states.append(state)
