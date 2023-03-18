from dict2xml import dict2xml


def format_output(dfa):
    output = {"dfa":dfa['dfa'], 'list_states':[]}
    new_states = []
    for i, state in enumerate(dfa['states']):
        new_states.append({"state":state['state'], 'transitions':[], 'accepting':state['accepting'], 'starting':state['starting']})
        items = []
        for j, _input in enumerate(state['input']):
            items.append({'input':state['input'][j], 'next_state':state['next_state'][j]['state']})
        new_states[i]['transitions'].append(items)
    output['list_states'] = new_states
    return output


def output_to_xml(dfa):
    with open('output.xml', 'w+') as file:
        file.write(dict2xml(format_output(dfa)))
