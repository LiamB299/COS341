import re
from definitions2 import non_terminals, terminals, rules
from classes import NfaState, NfaBlock
import uuid
from nfa_to_dfa import df_search, generate_basic_closures, generate_transition_table


def generate_label_name(prefix):
    return prefix
    # unique_id = str(uuid.uuid4()).replace('-', '')  # Generate a random UUID and remove the dashes
    # return f"{prefix}_{unique_id}"


def split_string(string, word_list):
    # Create a regex pattern that matches any word in the word list
    pattern = '|'.join(map(re.escape, word_list))

    # Split the string based on the pattern, keeping the delimiters
    parts = re.split(f'({pattern})', string)

    # Remove any empty parts and return the result
    return [part for part in parts if part]


def parse_rule(rule: str, block_number: int):
    prod_symbol, production = rule.replace(" ", "").split("::=")
    products = split_string(production, non_terminals + terminals)
    nfa_block = NfaBlock()
    nfa_block.expression = rule

    # prod symbol for epsilon transitions
    nfa_block.LHS_symbol = prod_symbol

    # generate base NFA blocks
    if products[0] == 'ε':
        final_state = NfaState("##", generate_label_name("S"+str(block_number)+"1"), False)
        final_state.finishing = True
        nfa_block.append_symbol(final_state)

    elif prod_symbol == 'C':
        state = NfaState("<ASCII>", generate_label_name("S"+str(block_number)+"1"), False)
        nfa_block.append_symbol(state)
        final_state = NfaState("##", generate_label_name("S"+str(block_number)+"2"), False)
        final_state.finishing = True
        nfa_block.append_symbol(final_state)

    else:
        for i, product in enumerate(products):
            state = NfaState(product, generate_label_name("S"+str(block_number)+str(i)), product not in non_terminals)
            nfa_block.append_symbol(state)
        final_state = NfaState("##", generate_label_name("S"+str(block_number)+str(i)), False)
        final_state.finishing = True
        nfa_block.append_symbol(final_state)

    return nfa_block


def generate_rule_blocks():
    nfa_blocks: [NfaBlock] = []
    for i, rule in enumerate(rules):
        nfa_blocks.append(parse_rule(rule, i))

    return nfa_blocks


def link_epsilons(nfa_blocks: [NfaBlock]):
    for block in nfa_blocks:
        # find RHS symbol
        current_symbol = block.start_symbol
        while current_symbol != 0:
            if not current_symbol.terminal_transition:
                # compare to LHS Prods to find links
                for compare_block in nfa_blocks:
                    if compare_block.LHS_symbol == current_symbol.symbol_transition:
                        current_symbol.epsilon_transitions.append(compare_block.start_symbol)
            current_symbol = current_symbol.next


rule_blocks = generate_rule_blocks()
link_epsilons(rule_blocks)
for block in rule_blocks:
    block.print_block()

visited = []
df_search(rule_blocks[4].start_symbol.next, visited)
print(visited)

trans_table = generate_transition_table(rule_blocks)
generate_basic_closures(trans_table)
