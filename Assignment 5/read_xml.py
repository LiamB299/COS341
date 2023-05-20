import xmltodict as parser


def read_tree(filename='output.xml'):
    with open(filename, 'r') as file:
        return parser.parse(file.read(), attr_prefix='', cdata_key='value')