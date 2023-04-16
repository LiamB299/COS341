from parse_tree import *


def traverse_tree(current_node: NT_node | T_node, file, indents):
    if not current_node.is_terminal:
        if len(current_node.children) == 0:
            file.write(indents + f'<{current_node.label} children=\'[]\'></{current_node.label}>')
            return

        ids = ''
        for child in current_node.children:
            ids += str(child.id) + ','
        ids = ids[:len(ids) - 1]

        file.write(indents + f'<{current_node.label} id=\'{current_node.id}\' children=\'[{ids}]\'>\n')
        old_indents = indents
        indents += '\t'
        for child in current_node.children:
            traverse_tree(child, file, indents)

        file.write(old_indents + f'</{current_node.label}>\n')
        indents = old_indents
        return

    else:
        file.write(indents + f'<terminal id=\'{current_node.id}\'>{current_node.label}</terminal>\n')


def write_to_xml(head_node: NT_node):
    file = open('output.xml', 'w+')
    traverse_tree(head_node, file, '')
    file.close()
