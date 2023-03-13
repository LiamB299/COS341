from lexer import print_dfa


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

        changed = no_duplicates_finishing and no_duplicates_unfinishing

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
            new_states.append({'state': 'n' + str(count),
                               'input': duplicate_set[0]['state']['input'],
                                'next_state': duplicate_set[0]['state']['next_state'],
                               'accepting': duplicate_set[0]['state']['accepting'],
                               'starting': starting,
                               "old_states": old_states})

        count += 1
        i = k + 1

    return new_states


# O(n^4)
def find_duplicates(states):
    duplicates = []
    count = 0
    for i, state in enumerate(states):
        count += 1
        for j in range(i + 1, len(states)):
            compare_state = states[j]
            same_state = True
            for k, _input in enumerate(state['input']):
                inner_broke = False
                for l, compare_input in enumerate(compare_state["input"]):
                    if _input == compare_input:
                        if state["next_state"][k]['state'] != compare_state['next_state'][l]['state']:
                            same_state = False
                            inner_broke = True
                            break

                if inner_broke:
                    break

                if same_state:
                    duplicates.append({"state": state, "group": count})
                    duplicates.append({"state": compare_state, "group": count})
                    break

    return duplicates


dfa = {
    'dfa': "un-minimized",
    'states': [
        {
            'state': '0',
            'input': [
                '0',
                '1'
            ],
            'next_state': [
                {
                    'state': '1',
                },
                {
                    'state': '3'
                }
            ],
            'starting': True,
            'accepting': False
        },
        {
            'state': '1',
            'input': [
                '0',
                '1'
            ],
            'next_state': [
                {
                    'state': '0',
                },
                {
                    'state': '3'
                }
            ],
            'starting': False,
            'accepting': False
        },
        {
            'state': '3',
            'input': [
                '0',
                '1'
            ],
            'next_state': [
                {
                    'state': '5',
                },
                {
                    'state': '5'
                }
            ],
            'starting': False,
            'accepting': True
        },
        {
            'state': '5',
            'input': [
                '0',
                '1'
            ],
            'next_state': [
                {
                    'state': '5',
                },
                {
                    'state': '5'
                }
            ],
            'starting': False,
            'accepting': True
        }
    ]
}

print_dfa(minimize(dfa))
