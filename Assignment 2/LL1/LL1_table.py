from definitions import *
import tabulate


def get_symbol_follow(symbol):
    for i, nt in enumerate(non_terminals):
        if nt == symbol:
            return follow[i]


def build_LL1_table():
    table = {}
    for i, production in enumerate(rules):
        prod_symbol, production = production.replace(" ", "").split("::=")
        for j, non_terminal in enumerate(non_terminals):
            if non_terminal == prod_symbol:
                for terminal in terminals:
                    if terminal in first[i]:
                        table[(prod_symbol, terminal)] = production
                    elif nullable[i] and terminal in follow[j]:
                        table[(prod_symbol, terminal)] = production

    # print_LL1_table(table)
    return table

# def build_LL1_table():
#     table = {}
#     for i, production in enumerate(rules):
#         prod_symbol, production = production.replace(" ", "").split("::=")
#         for terminal in terminals:
#             if terminal in first[i]:
#                 table[(prod_symbol, terminal)] = production
#             elif nullable[i] and terminal in get_symbol_follow(prod_symbol):
#                 table[(prod_symbol, terminal)] = production
#
#     print_LL1_table(table)
#     return table


def print_LL1_table(LL1_table):
    headings = ['inputs', 'productions']
    data = []
    for inputs, production in LL1_table.items():
        data.append([inputs, production])

    table = tabulate.tabulate(data, headings)
    print(table)
    print('\n')


# build_LL1_table()
