import xmltodict


def read_tree(filename='./output.xml'):
    with open(filename, 'r') as file:
        return xmltodict.parse(file.read())
    