from dict2xml import dict2xml


def output_to_xml(dfa):
    with open('output.xml', 'w+') as file:
        file.write(dict2xml(dfa))
